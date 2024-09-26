
from django.urls import path
from .views import UserRegistrationView,LoginView,TokenRefreshView

urlpatterns = [
    path('auth/signup/', UserRegistrationView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Custom token refresh endpoint
]