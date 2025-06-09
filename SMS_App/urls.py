from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthViewSet, UserViewSet, StudentProfileViewSet, SubjectViewSet, AttendanceViewSet,
    ExamResultViewSet, AssignmentViewSet, AssignmentSubmissionViewSet, NoticeViewSet,
    TeacherProfileViewSet, TimeTableViewSet, FeeViewSet
)

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'users', UserViewSet, basename='user')
router.register(r'student-profiles', StudentProfileViewSet, basename='studentprofile')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'exam-results', ExamResultViewSet, basename='examresult')
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'assignment-submissions', AssignmentSubmissionViewSet, basename='assignmentsubmission')
router.register(r'notices', NoticeViewSet, basename='notice')
router.register(r'teacher-profiles', TeacherProfileViewSet, basename='teacherprofile')
router.register(r'timetable', TimeTableViewSet, basename='timetable')
router.register(r'fees', FeeViewSet, basename='fee')

urlpatterns = [
    path('', include(router.urls)),
]