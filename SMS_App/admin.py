from django.contrib import admin
from .models import SchoolUser, StudentProfile, TeacherProfile, SchoolClass

@admin.register(SchoolUser)
class SchoolUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'user_type')
    list_filter = ('user_type', 'is_active', 'is_staff')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'admission_number', 'current_class', 'parent_contact')
    search_fields = ('user__email', 'admission_number', 'current_class')

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'staff_id', 'qualification')
    search_fields = ('user__email', 'staff_id', 'qualification')

@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_teacher', 'academic_year')
    search_fields = ('name', 'academic_year')
    list_filter = ('academic_year',)
