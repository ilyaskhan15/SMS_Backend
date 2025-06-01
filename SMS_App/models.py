from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class SchoolUserManager(BaseUserManager):
    """Custom manager for SchoolUser model."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular SchoolUser with email and password."""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class SchoolUser(AbstractUser):
    """Custom user model for the school management system."""
    
    username = None
    email = models.EmailField('Email Address', unique=True)
    
    # Basic user types
    class UserType(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        TEACHER = 'TEACHER', 'Teacher'
        STUDENT = 'STUDENT', 'Student'
        PARENT = 'PARENT', 'Parent'
    
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.STUDENT
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = SchoolUserManager()
    
    def __str__(self):
        return self.email

class PasswordResetToken(models.Model):
    """Model for password reset functionality."""
    user = models.ForeignKey(SchoolUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

class Student(models.Model):
    """Simplified student model for school management."""
    user = models.OneToOneField(SchoolUser, on_delete=models.CASCADE, primary_key=True)
    admission_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    current_class = models.CharField(max_length=50)  # e.g., "Class 5A" or "Grade 3"
    parent_contact = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.admission_number})"

class Teacher(models.Model):
    """Teacher model for school management."""
    user = models.OneToOneField(SchoolUser, on_delete=models.CASCADE, primary_key=True)
    staff_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    qualification = models.CharField(max_length=100, blank=True)
    subjects_taught = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.staff_id})"

class Class(models.Model):
    """Class model representing different classes/grades in the school."""
    name = models.CharField(max_length=50)  # e.g., "Class 1", "Grade 5B"
    class_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    academic_year = models.CharField(max_length=20)  # e.g., "2023-2024"
    
    def __str__(self):
        return f"{self.name} ({self.academic_year})"
# Create your models here.

class UserAccount(AbstractUser):
    """Custom user model for the school management system."""
    
    username = None
    email = models.EmailField('Email Address', unique=True)
    
    # Basic user types
    class UserType(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        TEACHER = 'TEACHER', 'Teacher'
        STUDENT = 'STUDENT', 'Student'
        PARENT = 'PARENT', 'Parent'
    
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.STUDENT
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = SchoolUserManager()
    
    def __str__(self):
        return self.email

class UserPasswordResetToken(models.Model):
    """Model for password reset functionality."""
    user = models.ForeignKey(SchoolUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

class StudentProfile(models.Model):
    """Simplified student model for school management."""
    user = models.OneToOneField(SchoolUser, on_delete=models.CASCADE, primary_key=True)
    admission_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    current_class = models.CharField(max_length=50)  # e.g., "Class 5A" or "Grade 3"
    parent_contact = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.admission_number})"

class TeacherProfile(models.Model):
    """Teacher model for school management."""
    user = models.OneToOneField(SchoolUser, on_delete=models.CASCADE, primary_key=True)
    staff_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    qualification = models.CharField(max_length=100, blank=True)
    subjects_taught = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.staff_id})"

class SchoolClass(models.Model):
    """Class model representing different classes/grades in the school."""
    name = models.CharField(max_length=50)  # e.g., "Class 1", "Grade 5B"
    class_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    academic_year = models.CharField(max_length=20)  # e.g., "2023-2024"
    
    def __str__(self):
        return f"{self.name} ({self.academic_year})"
# Create your models here.
