from django.urls import path
from .views import (
    StudentProfileListCreateView, StudentProfileRetrieveUpdateDestroyView,
    FeeListCreateView, FeeRetrieveUpdateDestroyView,
    AttendanceListCreateView, AttendanceRetrieveUpdateDestroyView, 
    StudentRegistrationView, SubjectListCreateView,
    ResultListCreateView, ResultRetrieveUpdateDestroyView,
    StudentLoginView
)

urlpatterns = [
    # Student authentication
    path('students/register/', StudentRegistrationView.as_view(), name='student-register'),
    path('students/login/', StudentLoginView.as_view(), name='student-login'),
    
    # Student profiles
    path('students/', StudentProfileListCreateView.as_view(), name='student-list-create'),
    path('students/<int:pk>/', StudentProfileRetrieveUpdateDestroyView.as_view(), name='student-detail'),
    
    # Financial management
    path('fees/', FeeListCreateView.as_view(), name='fee-list-create'),
    path('fees/<int:pk>/', FeeRetrieveUpdateDestroyView.as_view(), name='fee-detail'),
    
    # Attendance tracking
    path('attendances/', AttendanceListCreateView.as_view(), name='attendance-list-create'),
    path('attendances/<int:pk>/', AttendanceRetrieveUpdateDestroyView.as_view(), name='attendance-detail'),
    
    # Academic management
    path('subjects/', SubjectListCreateView.as_view(), name='subject-list-create'),
    path('results/', ResultListCreateView.as_view(), name='result-list-create'),
    path('results/<int:pk>/', ResultRetrieveUpdateDestroyView.as_view(), name='result-detail'),
]