from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import viewsets, status, permissions, mixins
from rest_framework.decorators import action
from django.contrib.auth import authenticate, get_user_model
from .models import Assignment, AssignmentSubmission, Attendance, ExamResult, Notice, PasswordResetToken, StudentProfile, Fee, SchoolUser, Subject, TeacherProfile, TimeTable
from .serializers import (
    AssignmentSerializer, AssignmentSubmissionSerializer, AttendanceSerializer, ExamResultSerializer, FeeSerializer, NoticeSerializer, RegisterSerializer, LoginSerializer, ForgotPasswordSerializer,
    ResetPasswordSerializer, SubjectSerializer, TeacherProfileSerializer, TimeTableSerializer, UserSerializer, StudentProfileSerializer
)
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

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
                expires_at = timezone.now() + timedelta(hours=1)
                PasswordResetToken.objects.create(user=user, token=token, expires_at=expires_at)
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

class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Students can only see their own profile
        user = self.request.user
        if user.user_type == SchoolUser.UserType.STUDENT:
            return StudentProfile.objects.filter(user=user)
        return super().get_queryset()

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

class AttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == SchoolUser.UserType.STUDENT:
            return Attendance.objects.filter(student__user=user)
        return super().get_queryset()

class ExamResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExamResult.objects.all()
    serializer_class = ExamResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == SchoolUser.UserType.STUDENT:
            return ExamResult.objects.filter(student__user=user)
        return super().get_queryset()

class AssignmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentSubmission.objects.all()
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == SchoolUser.UserType.STUDENT:
            return AssignmentSubmission.objects.filter(student__user=user)
        return super().get_queryset()

class NoticeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [permissions.IsAuthenticated]

class TeacherProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class TimeTableViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TimeTable.objects.all()
    serializer_class = TimeTableSerializer
    permission_classes = [permissions.IsAuthenticated]

class FeeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Fee.objects.all()
    serializer_class = FeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == SchoolUser.UserType.STUDENT:
            return Fee.objects.filter(student__user=user)
        return super().get_queryset()
