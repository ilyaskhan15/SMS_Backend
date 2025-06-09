from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings

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

class StudentProfile(models.Model):
    """Profile/details for a student."""
    user = models.OneToOneField(SchoolUser, on_delete=models.CASCADE, primary_key=True)
    admission_number = models.CharField(max_length=20, unique=True)
    current_class = models.CharField(max_length=50)  # e.g., "Class 10"
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    parent_name = models.CharField(max_length=100, blank=True)
    parent_phone = models.CharField(max_length=15, blank=True)
    photo = models.ImageField(upload_to='students/photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} (Class: {self.current_class})"

class Subject(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.email} - {self.date} - {self.status}"

class ExamResult(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=50)  # e.g., "Mid-Term", "Final"
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    remarks = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

    def percentage(self):
        return (self.marks_obtained / self.max_marks) * 100

    def __str__(self):
        return f"{self.student.user.email} - {self.subject.name} - {self.exam_name}"

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    assigned_by = models.ForeignKey(SchoolUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'TEACHER'})
    file = models.FileField(upload_to='assignments/', null=True, blank=True)

    def __str__(self):
        return self.title

class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    submitted_file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.email} - {self.assignment.title}"

class Notice(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(SchoolUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class TeacherProfile(models.Model):
    """Profile/details for a teacher."""
    user = models.OneToOneField(SchoolUser, on_delete=models.CASCADE, primary_key=True)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    photo = models.ImageField(upload_to='teacher_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class TimeTable(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.day} - {self.subject.name} ({self.start_time} to {self.end_time})"

class Fee(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.email} - {self.amount}"
