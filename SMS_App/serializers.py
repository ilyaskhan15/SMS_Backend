from rest_framework import serializers
from .models import (
    SchoolUser, StudentProfile, Subject, Attendance, ExamResult,
    Assignment, AssignmentSubmission, Notice, TimeTable, Fee, TeacherProfile
)

class RegisterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    confirmed_password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = SchoolUser
        fields = ['full_name', 'email', 'password', 'confirmed_password']

    def validate(self, data):
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError("Passwords do not match.")
        if SchoolUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return data

    def create(self, validated_data):
        full_name = validated_data.pop('full_name')
        password = validated_data.pop('password')
        validated_data.pop('confirmed_password')
        first_name = full_name.split(' ')[0]
        last_name = ' '.join(full_name.split(' ')[1:]) if len(full_name.split(' ')) > 1 else ''
        user = SchoolUser.objects.create(
            email=validated_data['email'],
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField()
    confirmed_password = serializers.CharField()

    def validate(self, data):
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolUser
        fields = ['id', 'email', 'first_name', 'last_name', 'user_type']

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            'user', 'admission_number', 'current_class', 'date_of_birth',
            'address', 'phone', 'parent_name', 'parent_phone', 'photo'
        ]

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code']

class AttendanceSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'date', 'status', 'subject']

class ExamResultSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    percentage = serializers.SerializerMethodField()

    class Meta:
        model = ExamResult
        fields = [
            'id', 'student', 'subject', 'exam_name', 'marks_obtained',
            'max_marks', 'remarks', 'date', 'percentage'
        ]

    def get_percentage(self, obj):
        return obj.percentage()

class AssignmentSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    assigned_by = UserSerializer(read_only=True)

    class Meta:
        model = Assignment
        fields = [
            'id', 'title', 'description', 'subject', 'due_date',
            'assigned_by', 'file'
        ]

class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    assignment = AssignmentSerializer(read_only=True)
    student = StudentProfileSerializer(read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = [
            'id', 'assignment', 'student', 'submitted_file',
            'submitted_at', 'remarks', 'marks_obtained'
        ]

class NoticeSerializer(serializers.ModelSerializer):
    posted_by = UserSerializer(read_only=True)

    class Meta:
        model = Notice
        fields = ['id', 'title', 'description', 'date_posted', 'posted_by']

class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TeacherProfile
        fields = [
            'user', 'employee_id', 'department', 'phone', 'address', 'photo'
        ]

class TimeTableSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    teacher = TeacherProfileSerializer(read_only=True)

    class Meta:
        model = TimeTable
        fields = [
            'id', 'day', 'subject', 'start_time', 'end_time', 'teacher'
        ]

class FeeSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(read_only=True)

    class Meta:
        model = Fee
        fields = [
            'id', 'student', 'amount', 'due_date', 'paid', 'payment_date'
        ]