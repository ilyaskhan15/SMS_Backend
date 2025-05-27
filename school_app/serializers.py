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