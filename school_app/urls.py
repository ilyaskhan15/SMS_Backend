from django.urls import path
from .views import (
    StudentProfileListCreateView,
    StudentProfileRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('students/', StudentProfileListCreateView.as_view(), name='studentprofile-list-create'),
    path('students/<int:pk>/', StudentProfileRetrieveUpdateDestroyView.as_view(), name='studentprofile-detail'),
]