from django.urls import path
from account import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'account'
urlpatterns = [
    # Account
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.Register.as_view(), name='register'),
    path('confirm-account/<int:key>/', views.confirm_account, name='confirm_account'),
    path('profile/auth/', views.CurrentProfile.as_view(), name='auth_user'),
    path('profile/<int:user_pk>/', views.Profile.as_view(), name='profile'),
    path('photo_of_user/', views.PublishPhotoOfUser.as_view(), name='publish_photo'),
    path('photo_of_user/<int:photo_pk>/', views.DeletePhotoOfUser.as_view(), name='delete_photo'),
]
