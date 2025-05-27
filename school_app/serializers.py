from rest_framework import serializers
from .models import Student
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class StudentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Student
        fields = [
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'roll_number',
            'grade'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def create(self, validated_data):
        student = Student.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            roll_number=validated_data['roll_number'],
            grade=validated_data['grade']
        )
        return student

class StudentLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.email,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'roll_number': self.user.roll_number,
                'grade': self.user.grade
            }
        })
        return data