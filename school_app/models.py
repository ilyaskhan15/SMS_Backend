# models.py
from django.contrib.auth.models import User
from django.db import models

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=20, unique=True)
    grade = models.CharField(max_length=10)
    section = models.CharField(max_length=5, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    admission_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='static/student_profiles', blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"
