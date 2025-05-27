from django.contrib.auth.models import AbstractUser
from django.db import models

class Student(AbstractUser):
    roll_number = models.CharField(max_length=20, unique=True)
    grade = models.CharField(max_length=10)

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'roll_number', 'grade']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"