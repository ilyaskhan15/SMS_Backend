from rest_framework import serializers
from django.contrib.auth.models import User
from .models import StudentProfile, Fee, Attendance, Subject, Result
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            'id', 'user', 'roll_number', 'grade', 'section', 'phone',
            'address', 'date_of_birth', 'admission_date', 'profile_picture'
        ]

class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fee
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'

class StudentRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = StudentProfile
        fields = ['email', 'password']

    def validate_email(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        user = User.objects.create(username=email, email=email, is_active=False)
        user.set_password(password)
        user.save()
        student_profile = StudentProfile.objects.create(user=user, **validated_data)
        self.send_verification_email(user)
        return student_profile

    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        uid = user.pk
        verification_url = self.context['request'].build_absolute_uri(
            reverse('verify-email', kwargs={'uid': uid, 'token': token})
        )
        send_mail(
            'Verify your email address',
            f'Click the link to verify your email: {verification_url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

class StudentLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()