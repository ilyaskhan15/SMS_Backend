from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import StudentRegistrationSerializer, StudentLoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterStudentView(generics.CreateAPIView):
    serializer_class = StudentRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        
        return Response({
            'message': 'Student registered successfully',
            'student': {
                'id': student.id,
                'username': student.username,
                'email': student.email,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'roll_number': student.roll_number,
                'grade': student.grade
            }
        }, status=status.HTTP_201_CREATED)

class StudentLoginView(TokenObtainPairView):
    serializer_class = StudentLoginSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data
        data['message'] = "You are enter temporary"
        return Response(data, status=status.HTTP_200_OK)