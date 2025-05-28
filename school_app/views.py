from rest_framework import generics, permissions
from .serializers import StudentRegistrationSerializer, StudentProfileSerializer
from .models import StudentProfile

class StudentRegistrationView(generics.CreateAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class StudentProfileListCreateView(generics.ListCreateAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class StudentProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]