from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentRegistrationSerializer, StudentProfileSerializer, StudentLoginSerializer
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

class StudentLoginView(APIView):
    def post(self, request):
        serializer = StudentLoginSerializer(data=request.data)
        if serializer.is_valid():
            roll_number = serializer.validated_data['roll_number']
            email = serializer.validated_data['email']
            try:
                student = StudentProfile.objects.get(roll_number=roll_number)
                if student.user.email == email:
                    return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
            except StudentProfile.DoesNotExist:
                return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)