from django.contrib import admin
from .models import StudentProfile, Fee, Attendance, Subject, Result

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'grade', 'section', 'phone')
    search_fields = ('user__username', 'roll_number', 'grade', 'section')

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'due_date', 'is_paid')
    search_fields = ('student__roll_number',)
    list_filter = ('is_paid', 'due_date')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status')
    search_fields = ('student__roll_number', 'status')
    list_filter = ('status', 'date')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'exam_name', 'marks', 'grade', 'date')
    search_fields = ('student__roll_number', 'subject__name', 'exam_name')
    list_filter = ('grade', 'date')