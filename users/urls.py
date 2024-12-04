from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import LogoutView, RegisterView, UserProfileView, UserProfileViewSet, UserReviewsView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='user-profile')

urlpatterns = [
    # Register URL
    path('register/', RegisterView.as_view(), name='register'),
    
    # Login URL for JWT
    path('login/', TokenObtainPairView.as_view(), name='login'),
    
    # Token Refresh URL
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Logout URL
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Profile and related actions (only accessible to authenticated users)
    path('profile/', UserProfileViewSet.as_view({'get': 'retrieve', 'post': 'update_avatar'}), name='profile'),
    path('me/', UserProfileViewSet.as_view({'get': 'me'}), name='me'),
    path('favorites/', UserProfileViewSet.as_view({'get': 'favorites'}), name='favorites'),
    path('reviews/', UserProfileViewSet.as_view({'get': 'reviews'}), name='reviews'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('<int:pk>/reviews/', UserReviewsView.as_view(), name='user-reviews'),
    path('toggle-favorite/', 
         UserProfileViewSet.as_view({'post': 'toggle_favorite'}), 
         name='toggle-favorite'),
    # Include the router's URLs for the rest of the profile-related actions
    path('', include(router.urls)),
]
