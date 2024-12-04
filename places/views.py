from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Avg
from .models import Category, Place, Review
from .serializers import (
    CategorySerializer, PlaceSerializer, 
    PlaceDetailSerializer, ReviewSerializer
)
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all().annotate(
        avg_rating=Avg('reviews__rating')
    )
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'address', 'category__name']
    ordering_fields = ['avg_rating', 'created_at', 'name']
    def get_queryset(self):
        queryset = Place.objects.all().annotate(
            avg_rating=Avg('reviews__rating')
        )
        
        # Get category from query params
        category = self.request.query_params.get('category', None)
        if category and category != 'all':
            queryset = queryset.filter(category__id=category)  # Assuming category is the Category model FK

        return queryset
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PlaceDetailSerializer
        return PlaceSerializer
    @action(detail=True, methods=['GET', 'POST'])
    def reviews(self, request, pk=None):
        place = self.get_object()
        
        if request.method == 'GET':
            reviews = place.reviews.all()
            serializer = ReviewSerializer(reviews, many=True, context={'request': request})
            return Response(serializer.data)
            
        elif request.method == 'POST':
            user = request.user

            # Check if user already reviewed this place
            if place.reviews.filter(user=user).exists():
                return Response(
                    {'error': 'You have already reviewed this place'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate request data
            rating = request.data.get('rating')
            comment = request.data.get('comment')

            if not rating or not comment:
                return Response(
                    {'error': 'Both rating and comment are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                # Create review
                review = Review.objects.create(
                    place=place,
                    user=user,
                    rating=rating,
                    comment=comment
                )

                # Update place site rating
                place.update_site_rating()
                place.review_count = place.reviews.count()
                place.save()

                # Return the created review
                serializer = ReviewSerializer(review)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                print("Error creating review:", str(e))
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
    @action(detail=True, methods=['post'])
    def upload_images(self, request, pk=None):
        place = self.get_object()
        images = request.FILES.getlist('images')
        is_primary = request.data.get('is_primary', False)

        for image in images:
            PlaceImage.objects.create(
                place=place,
                image=image,
                is_primary=is_primary
            )

        return Response({'status': 'Images uploaded'}, status=status.HTTP_201_CREATED)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PlaceReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        place_id = self.kwargs.get('place_id')
        place = get_object_or_404(Place, id=place_id)
        serializer.save(user=self.request.user, place=place)