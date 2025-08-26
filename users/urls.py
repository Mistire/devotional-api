from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import EmailTokenObtainPairView, RegisterView, ProfileView


urlpatterns = [
  path('register/', RegisterView.as_view(), name='register'),
  path('login/', EmailTokenObtainPairView.as_view(), name='login'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('profile/', ProfileView.as_view(), name='profile'),

  
]