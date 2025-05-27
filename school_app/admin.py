from django.contrib import admin
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'grade', 'section', 'phone')
    search_fields = ('user__username', 'roll_number', 'grade', 'section')