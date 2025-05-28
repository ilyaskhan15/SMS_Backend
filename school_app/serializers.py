from rest_framework import serializers
from django.contrib.auth.models import User
from .models import StudentProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StudentProfile
        fields = [
            'id',
            'user',
            'roll_number',
            'grade',
            'section',
            'phone',
            'address',
            'date_of_birth',
            'admission_date',
            'profile_picture',
        ]

class StudentRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = StudentProfile
        fields = [
            'username', 'password', 'email', 'first_name', 'last_name',
            'roll_number', 'grade', 'section', 'phone', 'address',
            'date_of_birth', 'admission_date', 'profile_picture'
        ]

    def create(self, validated_data):
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
        }
        password = validated_data.pop('password')
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()
        student_profile = StudentProfile.objects.create(user=user, **validated_data)
        return student_profile