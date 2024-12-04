from rest_framework import generics, status, permissions, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import action
from places.models import Place, Review
from places.serializers import PlaceSerializer, ReviewSerializer
from .serializers import RegisterSerializer, UserProfileSerializer, UserDetailSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

from rest_framework import generics

# views.py
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]  # Or appropriate permission

    def get_object(self):
        pk = self.kwargs.get('pk')  # Change from user_id to pk
        return get_object_or_404(User, id=pk)  # Use get_object_or_404

class UserReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]  # Or appropriate permission

    def get_queryset(self):
        pk = self.kwargs.get('pk')  # Change from user_id to pk
        return Review.objects.filter(user_id=pk)

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'me']:
            return UserDetailSerializer
        return UserProfileSerializer
    
    @action(detail=False, methods=['GET'])
    def favorites(self, request):
        user = request.user
        favorites = user.favorite_places.all()
        serializer = PlaceSerializer(favorites, many=True, context={'request': request})
        return Response({
            'results': serializer.data,
            'count': favorites.count()
        })

    @action(detail=False, methods=['post'])
    def toggle_favorite(self, request):
        try:
            place_id = request.data.get('place_id')
            if not place_id:
                return Response(
                    {'error': 'place_id is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            place = get_object_or_404(Place, id=place_id)
            user = request.user

            if user.favorite_places.filter(id=place_id).exists():
                user.favorite_places.remove(place)
                is_favorite = False
            else:
                user.favorite_places.add(place)
                is_favorite = True

            return Response({
                'is_favorite': is_favorite,
                'message': 'Place successfully added to favorites' if is_favorite 
                          else 'Place successfully removed from favorites'
            })

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get', 'put', 'patch','post'])
    def update_avatar(self, request):
        if 'avatar' not in request.FILES:
            return Response({'error': 'No avatar file provided'}, status=400)
        
        user = request.user
        user.avatar = request.FILES['avatar']
        user.save()
        
        return Response({'message': 'Avatar updated successfully'})
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        # For PUT and PATCH requests
        print("Received data:", request.data)  # Add this for debugging
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            print("Valid data:", serializer.validated_data)  # Add this for debugging
            user = serializer.save()
            print("Saved user:", user)  # Add this for debugging
            return Response(serializer.data)
        print("Validation errors:", serializer.errors)  # Add this for debugging
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
