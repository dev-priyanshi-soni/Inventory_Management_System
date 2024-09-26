from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            return Response({
                'access': str(access_token),
                'refresh': str(refresh),
                'user_id': user.id
            }, status=status.HTTP_200_OK)
        
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            access_token = token.access_token 

            return Response({
                'access': str(access_token)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Invalid or expired refresh token."}, status=status.HTTP_401_UNAUTHORIZED)