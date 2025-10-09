from rest_framework import routers
from . import views
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'teachers', views.TeacherViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'enrollments', views.EnrollmentViewSet)
router.register(r'attendance', views.AttendanceViewSet)
router.register(r'grades', views.GradeViewSet)

urlpatterns = [
    # Template views
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    
    # Management views
    path('students/', views.student_list_view, name='student_list'),
    path('teachers/', views.teacher_list_view, name='teacher_list'),
    path('courses/', views.course_list_view, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail_view, name='course_detail'),
    path('my-students/', views.teacher_students_view, name='teacher_students'),
    
    # Student views
    path('my-attendance/', views.my_attendance_view, name='my_attendance'),
    path('my-grades/', views.my_grades_view, name='my_grades'),
    
    # Teacher views
    path('attendance/mark/', views.attendance_mark_view, name='attendance_mark'),
    path('attendance/entry/', views.attendance_entry_view, name='attendance_entry'),
    path('grades/entry/', views.grade_entry_view, name='grade_entry'),
    path('grades/bulk/<int:course_id>/', views.bulk_grade_entry_view, name='bulk_grade_entry'),
    
    # AJAX endpoints
    path('get-course-students/<int:course_id>/', views.get_course_students, name='get_course_students'),
    path('calculate-grade/', views.calculate_grade_ajax, name='calculate_grade_ajax'),
    
    # API endpoints
    path('api/', include(router.urls)),
]
