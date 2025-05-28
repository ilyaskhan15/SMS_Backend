from django.urls import path
from .views import (
    StudentProfileListCreateView, StudentProfileRetrieveUpdateDestroyView,
    FeeListCreateView, FeeRetrieveUpdateDestroyView,
    AttendanceListCreateView, AttendanceRetrieveUpdateDestroyView,
    SubjectListCreateView, SubjectRetrieveUpdateDestroyView,
    ResultListCreateView, ResultRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('students/', StudentProfileListCreateView.as_view(), name='student-list-create'),
    path('students/<int:pk>/', StudentProfileRetrieveUpdateDestroyView.as_view(), name='student-detail'),
    path('fees/', FeeListCreateView.as_view(), name='fee-list-create'),
    path('fees/<int:pk>/', FeeRetrieveUpdateDestroyView.as_view(), name='fee-detail'),
    path('attendances/', AttendanceListCreateView.as_view(), name='attendance-list-create'),
    path('attendances/<int:pk>/', AttendanceRetrieveUpdateDestroyView.as_view(), name='attendance-detail'),
    path('subjects/', SubjectListCreateView.as_view(), name='subject-list-create'),
    path('subjects/<int:pk>/', SubjectRetrieveUpdateDestroyView.as_view(), name='subject-detail'),
    path('results/', ResultListCreateView.as_view(), name='result-list-create'),
    path('results/<int:pk>/', ResultRetrieveUpdateDestroyView.as_view(), name='result-detail'),
]