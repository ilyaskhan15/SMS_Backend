# models.py
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=20, unique=True)
    grade = models.CharField(max_length=10)
    section = models.CharField(max_length=5, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    admission_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"

class Fee(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='fees')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"Fee for {self.student} - {self.amount}"

class Attendance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ])
    remarks = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Result(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=100)
    marks = models.DecimalField(max_digits=5, decimal_places=2, 
                              validators=[MinValueValidator(0), MaxValueValidator(100)])
    grade = models.CharField(max_length=2, blank=True)
    remarks = models.TextField(blank=True)
    date = models.DateField()
    
    def save(self, *args, **kwargs):
        # Auto calculate grade based on marks
        if self.marks >= 90:
            self.grade = 'A'
        elif self.marks >= 80:
            self.grade = 'B'
        elif self.marks >= 70:
            self.grade = 'C'
        elif self.marks >= 60:
            self.grade = 'D'
        else:
            self.grade = 'F'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student} - {self.subject} - {self.exam_name} - {self.marks}"
