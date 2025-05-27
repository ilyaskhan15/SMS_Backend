from django.urls import path
from django.contrib import admin
from .views import (
    RegisterStudentView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)
from django.contrib.auth.admin import UserAdmin
from .models import Student

@admin.register(Student)
class StudentAdmin(UserAdmin):
    model = Student
    list_display = ('email', 'username', 'first_name', 'last_name', 'roll_number', 'grade', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'roll_number', 'grade')
    ordering = ('email',)

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('roll_number', 'grade')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('roll_number', 'grade')}),
    )

urlpatterns = [
    # Admin Interface
    path('admin/', admin.site.urls),
    
    # Authentication Endpoints
    path('api/auth/register/', RegisterStudentView.as_view(), name='student-register'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/auth/verify/', TokenVerifyView.as_view(), name='token-verify'),
    
    
    # Add more student-related endpoints as needed
]