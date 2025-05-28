from django.urls import path
from .views import (
    StudentProfileListCreateView,
    StudentProfileRetrieveUpdateDestroyView,
    StudentRegistrationView,
    StudentLoginView,
)

urlpatterns = [
    path('students/', StudentProfileListCreateView.as_view(), name='studentprofile-list-create'),
    path('students/<int:pk>/', StudentProfileRetrieveUpdateDestroyView.as_view(), name='studentprofile-detail'),
    path('register/', StudentRegistrationView.as_view(), name='student-register'),
    path('login/', StudentLoginView.as_view(), name='student-login'),
]