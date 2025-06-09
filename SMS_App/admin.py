from django.contrib import admin
from .models import (
    SchoolUser, StudentProfile, Subject, Attendance, ExamResult,
    Assignment, AssignmentSubmission, Notice, TimeTable, Fee, TeacherProfile
)

@admin.register(SchoolUser)
class SchoolUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'user_type')
    list_filter = ('user_type', 'is_active', 'is_staff')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'admission_number', 'current_class', 'parent_name', 'parent_phone')
    search_fields = ('user__email', 'admission_number', 'current_class', 'parent_name')

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department', 'phone')
    search_fields = ('user__email', 'employee_id', 'department')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'subject')
    search_fields = ('student__user__email', 'date', 'status', 'subject__name')
    list_filter = ('status', 'date')

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'exam_name', 'marks_obtained', 'max_marks', 'date')
    search_fields = ('student__user__email', 'subject__name', 'exam_name')
    list_filter = ('subject', 'exam_name', 'date')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'due_date', 'assigned_by')
    search_fields = ('title', 'subject__name', 'assigned_by__email')
    list_filter = ('subject', 'due_date')

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'marks_obtained')
    search_fields = ('assignment__title', 'student__user__email')
    list_filter = ('submitted_at',)

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'posted_by')
    search_fields = ('title', 'posted_by__email')
    list_filter = ('date_posted',)

@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    list_display = ('day', 'subject', 'start_time', 'end_time', 'teacher')
    search_fields = ('day', 'subject__name', 'teacher__user__email')
    list_filter = ('day', 'subject')

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'due_date', 'paid', 'payment_date')
    search_fields = ('student__user__email',)
    list_filter = ('paid', 'due_date')
