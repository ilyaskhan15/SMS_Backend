from django.urls import path
from .views import RegisterStudentView, StudentLoginView

urlpatterns = [
    path('register/', RegisterStudentView.as_view(), name='student-register'),
    path('login/', StudentLoginView.as_view(), name='student-login'),
]