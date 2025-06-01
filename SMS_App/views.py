from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import viewsets, status, permissions, mixins
from rest_framework.decorators import action
from django.contrib.auth import authenticate, get_user_model
from .models import PasswordResetToken
from .serializers import (
    RegisterSerializer, LoginSerializer, ForgotPasswordSerializer,
    ResetPasswordSerializer, UserSerializer
)
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

class AuthViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'register':
            return RegisterSerializer
        if self.action == 'login':
            return LoginSerializer
        if self.action == 'forgot_password':
            return ForgotPasswordSerializer
        if self.action == 'reset_password':
            return ResetPasswordSerializer
        if self.action == 'me':
            return UserSerializer
        return RegisterSerializer  # Default fallback

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration successful.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if not user.is_active:
                    return Response({'error': 'Account is inactive.'}, status=status.HTTP_403_FORBIDDEN)
                return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='forgot-password')
    def forgot_password(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                token = get_random_string(64)
                PasswordResetToken.objects.create(user=user, token=token, expires_at=None)
                reset_link = f"http://localhost:8000/api/auth/reset-password?token={token}"
                send_mail(
                    'Password Reset',
                    f'Use this link to reset your password: {reset_link}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=True,
                )
            except User.DoesNotExist:
                pass
            return Response({'message': 'If the email exists, a reset link has been sent.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='reset-password')
    def reset_password(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            try:
                reset_token = PasswordResetToken.objects.get(token=token, is_used=False)
                user = reset_token.user
                user.set_password(serializer.validated_data['password'])
                user.save()
                reset_token.is_used = True
                reset_token.save()
                return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)
            except PasswordResetToken.DoesNotExist:
                return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='me', permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
