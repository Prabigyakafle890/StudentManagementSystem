from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Student, Teacher, Course, Enrollment, Attendance, Grade
from .serializers import (
    StudentSerializer, TeacherSerializer, CourseSerializer,
    EnrollmentSerializer, AttendanceSerializer, GradeSerializer
)
from .permissions import IsAdmin, IsTeacher, IsStudent, IsTeacherOrAdmin, IsOwnerOrAdmin
from .forms import GradeEntryForm, BulkGradeEntryForm, AttendanceEntryForm, BulkAttendanceForm


# Template Views
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    context = {
        'user': request.user,
    }
    
    if request.user.is_staff:
        # Admin dashboard data
        context.update({
            'total_students': Student.objects.count(),
            'total_teachers': Teacher.objects.count(),
            'total_courses': Course.objects.count(),
            'total_enrollments': Enrollment.objects.count(),
        })
    elif hasattr(request.user, 'teacher'):
        # Teacher dashboard data
        teacher_courses = Course.objects.filter(teacher=request.user.teacher)
        grades_entered = Grade.objects.filter(course__teacher=request.user.teacher).count()
        
        # Count students enrolled in this teacher's courses
        enrolled_student_ids = Enrollment.objects.filter(course__teacher=request.user.teacher).values_list('student_id', flat=True).distinct()
        total_students_count = len(enrolled_student_ids)
        
        context.update({
            'my_courses': teacher_courses,
            'teacher_courses': teacher_courses,
            'total_students': total_students_count,
            'grades_entered': grades_entered,
        })
    elif hasattr(request.user, 'student'):
        # Student dashboard data
        student_enrollments = Enrollment.objects.filter(student=request.user.student)
        student_grades = Grade.objects.filter(student=request.user.student)
        total_attendance = Attendance.objects.filter(student=request.user.student).count()
        present_attendance = Attendance.objects.filter(student=request.user.student, status='Present').count()
        attendance_percentage = round((present_attendance / total_attendance * 100) if total_attendance > 0 else 0)
        
        context.update({
            'my_enrollments': student_enrollments,
            'enrolled_courses': student_enrollments,
            'total_grades': student_grades.count(),
            'attendance_percentage': attendance_percentage,
            'recent_grades': student_grades.order_by('-id')[:5],  # using -id instead of -created_at
        })
    
    return render(request, 'core/dashboard.html', context)


@login_required
def profile_view(request):
    return render(request, 'core/profile.html', {'user': request.user})


@login_required 
def student_list_view(request):
    if not (request.user.is_staff or hasattr(request.user, 'teacher')):
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    students = Student.objects.all()
    return render(request, 'core/student_list.html', {'students': students})


@login_required
def teacher_list_view(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    teachers = Teacher.objects.all()
    return render(request, 'core/teacher_list.html', {'teachers': teachers})


@login_required
def course_list_view(request):
    if not (request.user.is_staff or hasattr(request.user, 'teacher') or hasattr(request.user, 'student')):
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    if hasattr(request.user, 'teacher'):
        # Teacher can only see their own courses
        courses = Course.objects.filter(teacher=request.user.teacher)
        context = {'courses': courses}
    elif hasattr(request.user, 'student'):
        # Student can see courses they're enrolled in
        enrollments = Enrollment.objects.filter(student=request.user.student)
        courses = [enrollment.course for enrollment in enrollments]
        context = {'courses': courses, 'enrollments': enrollments}
    else:
        # Staff can see all courses
        courses = Course.objects.all()
        context = {'courses': courses}
    
    return render(request, 'core/course_list.html', context)


@login_required
def teacher_students_view(request):
    if not hasattr(request.user, 'teacher'):
        messages.error(request, 'You must be a teacher to view this page.')
        return redirect('dashboard')
    
    # Get all students enrolled in this teacher's courses
    teacher_courses = Course.objects.filter(teacher=request.user.teacher)
    enrolled_students = Student.objects.filter(
        enrollment__course__in=teacher_courses
    ).distinct()
    
    return render(request, 'core/teacher_students.html', {
        'students': enrolled_students,
        'teacher_courses': teacher_courses
    })


@login_required
def course_detail_view(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        enrollments = Enrollment.objects.filter(course=course)
        return render(request, 'core/course_detail.html', {
            'course': course, 
            'enrollments': enrollments
        })
    except Course.DoesNotExist:
        messages.error(request, 'Course not found.')
        return redirect('dashboard')


@login_required
def my_attendance_view(request):
    if not hasattr(request.user, 'student'):
        messages.error(request, 'You must be a student to view this page.')
        return redirect('dashboard')
    
    attendance_records = Attendance.objects.filter(student=request.user.student).order_by('-date')
    
    # Calculate attendance statistics
    present_count = attendance_records.filter(status='Present').count()
    absent_count = attendance_records.filter(status='Absent').count()
    total_records = attendance_records.count()
    
    attendance_percentage = round((present_count / total_records * 100) if total_records > 0 else 0, 1)
    
    return render(request, 'core/my_attendance.html', {
        'attendance_records': attendance_records,
        'present_count': present_count,
        'absent_count': absent_count,
        'attendance_percentage': attendance_percentage
    })


@login_required
def my_grades_view(request):
    if not hasattr(request.user, 'student'):
        messages.error(request, 'You must be a student to view this page.')
        return redirect('dashboard')
    
    grades = Grade.objects.filter(student=request.user.student).select_related('course', 'course__teacher')
    
    # Calculate grade statistics using Nepali grading system
    if grades:
        total_marks = sum(grade.marks for grade in grades)
        average_marks = total_marks / len(grades)
        total_courses = grades.count()
        
        # Calculate GPA using the new student.gpa property
        gpa = request.user.student.gpa
        
        # Get highest grade using Nepali grading system
        nepali_grade_list = ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D+', 'D', 'E']
        highest_grade = min((grade.grade for grade in grades), key=lambda x: nepali_grade_list.index(x) if x in nepali_grade_list else 99)
        
        # Grade distribution
        grade_distribution = {}
        for grade in grades:
            if grade.grade in grade_distribution:
                grade_distribution[grade.grade] += 1
            else:
                grade_distribution[grade.grade] = 1
    else:
        average_marks = 0
        total_courses = 0
        highest_grade = 'N/A'
        gpa = 0.0
        grade_distribution = {}
    
    return render(request, 'core/my_grades.html', {
        'grades': grades,
        'average_marks': average_marks,
        'total_courses': total_courses,
        'highest_grade': highest_grade,
        'gpa': gpa,
        'grade_distribution': grade_distribution
    })


@login_required
def attendance_mark_view(request):
    if not (request.user.is_staff or hasattr(request.user, 'teacher')):
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    # Get statistics for teacher
    if hasattr(request.user, 'teacher'):
        teacher_courses = Course.objects.filter(teacher=request.user.teacher)
        total_students = Student.objects.filter(enrollment__course__in=teacher_courses).distinct().count()
        total_courses = teacher_courses.count()
    else:
        total_students = Student.objects.count()
        total_courses = Course.objects.count()
    
    return render(request, 'core/attendance_mark.html', {
        'total_students': total_students,
        'total_courses': total_courses
    })


@login_required
def grade_entry_view(request):
    if not (request.user.is_staff or hasattr(request.user, 'teacher')):
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    teacher = None
    if hasattr(request.user, 'teacher'):
        teacher = request.user.teacher
    
    # Handle single grade entry form
    grade_form = GradeEntryForm(teacher=teacher)
    bulk_form = BulkGradeEntryForm(teacher=teacher)
    
    if request.method == 'POST':
        if 'single_grade' in request.POST:
            grade_form = GradeEntryForm(request.POST, teacher=teacher)
            if grade_form.is_valid():
                grade = grade_form.save()
                messages.success(request, f'Grade successfully entered for {grade.student.name} in {grade.course.name}')
                return redirect('grade_entry')
        
        elif 'bulk_grade' in request.POST:
            bulk_form = BulkGradeEntryForm(request.POST, teacher=teacher)
            if bulk_form.is_valid():
                course = bulk_form.cleaned_data['course']
                return redirect('bulk_grade_entry', course_id=course.id)
    
    # Get existing grades
    if teacher:
        teacher_courses = Course.objects.filter(teacher=teacher)
        grades = Grade.objects.filter(course__in=teacher_courses).select_related('student', 'course')
    else:
        grades = Grade.objects.all().select_related('student', 'course')
    
    # Grade statistics
    a_grades = grades.filter(grade__in=['A+', 'A', 'A-']).count()
    b_grades = grades.filter(grade__in=['B+', 'B', 'B-']).count()
    c_grades = grades.filter(grade__in=['C+', 'C', 'C-']).count()
    d_grades = grades.filter(grade='D').count()
    f_grades = grades.filter(grade='F').count()
    
    return render(request, 'core/grade_entry.html', {
        'grade_form': grade_form,
        'bulk_form': bulk_form,
        'grades': grades,
        'a_grades': a_grades,
        'b_grades': b_grades,
        'c_grades': c_grades,
        'd_grades': d_grades,
        'f_grades': f_grades,
        'teacher': teacher
    })


@login_required
def bulk_grade_entry_view(request, course_id):
    if not (request.user.is_staff or hasattr(request.user, 'teacher')):
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    course = get_object_or_404(Course, id=course_id)
    teacher = None
    
    if hasattr(request.user, 'teacher'):
        teacher = request.user.teacher
        if course.teacher != teacher:
            messages.error(request, 'You can only enter grades for your own courses.')
            return redirect('grade_entry')
    
    # Get enrolled students
    enrollments = Enrollment.objects.filter(course=course).select_related('student')
    students = [enrollment.student for enrollment in enrollments]
    
    if request.method == 'POST':
        success_count = 0
        error_count = 0
        
        for student in students:
            marks_key = f'marks_{student.id}'
            grade_key = f'grade_{student.id}'
            
            if marks_key in request.POST and request.POST[marks_key]:
                try:
                    marks = float(request.POST[marks_key])
                    grade_letter = request.POST.get(grade_key, '')
                    
                    # Create or update grade
                    grade, created = Grade.objects.update_or_create(
                        student=student,
                        course=course,
                        defaults={
                            'marks': marks,
                            'grade': grade_letter
                        }
                    )
                    success_count += 1
                except (ValueError, TypeError):
                    error_count += 1
        
        if success_count > 0:
            messages.success(request, f'Successfully entered/updated {success_count} grades.')
        if error_count > 0:
            messages.error(request, f'Failed to process {error_count} grades. Please check your input.')
        
        return redirect('grade_entry')
    
    # Get existing grades for this course
    existing_grades = {
        grade.student.id: grade 
        for grade in Grade.objects.filter(course=course)
    }
    
    return render(request, 'core/bulk_grade_entry.html', {
        'course': course,
        'students': students,
        'existing_grades': existing_grades,
    })


@login_required
def attendance_entry_view(request):
    if not (request.user.is_staff or hasattr(request.user, 'teacher')):
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    teacher = None
    if hasattr(request.user, 'teacher'):
        teacher = request.user.teacher
    
    # Handle attendance entry form
    attendance_form = AttendanceEntryForm(teacher=teacher)
    bulk_attendance_form = BulkAttendanceForm(teacher=teacher)
    
    if request.method == 'POST':
        if 'single_attendance' in request.POST:
            attendance_form = AttendanceEntryForm(request.POST, teacher=teacher)
            if attendance_form.is_valid():
                attendance = attendance_form.save()
                messages.success(request, f'Attendance marked for {attendance.student.name}')
                return redirect('attendance_entry')
        
        elif 'bulk_attendance' in request.POST:
            bulk_attendance_form = BulkAttendanceForm(request.POST, teacher=teacher)
            if bulk_attendance_form.is_valid():
                course = bulk_attendance_form.cleaned_data['course']
                date = bulk_attendance_form.cleaned_data['date']
                return redirect('bulk_attendance_entry', course_id=course.id, date=date.strftime('%Y-%m-%d'))
    
    # Get recent attendance records
    if teacher:
        teacher_courses = Course.objects.filter(teacher=teacher)
        attendance_records = Attendance.objects.filter(course__in=teacher_courses).select_related('student', 'course').order_by('-date')[:20]
    else:
        attendance_records = Attendance.objects.all().select_related('student', 'course').order_by('-date')[:20]
    
    return render(request, 'core/attendance_entry.html', {
        'attendance_form': attendance_form,
        'bulk_attendance_form': bulk_attendance_form,
        'attendance_records': attendance_records,
        'teacher': teacher
    })


# AJAX helper views
@login_required
def get_course_students(request, course_id):
    """AJAX endpoint to get students enrolled in a course"""
    if not (request.user.is_staff or hasattr(request.user, 'teacher')):
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    course = get_object_or_404(Course, id=course_id)
    students = Student.objects.filter(enrollment__course=course).values('id', 'name', 'student_id')
    
    return JsonResponse({'students': list(students)})


@login_required
def calculate_grade_ajax(request):
    """AJAX endpoint to calculate grade from marks using Nepali grading system"""
    if request.method == 'POST':
        try:
            marks = float(request.POST.get('marks', 0))
            
            # Use Nepali grading system
            from core.utils.grading import calculate_nepali_grade
            grade, grade_point = calculate_nepali_grade(marks)
            
            return JsonResponse({
                'grade': grade,
                'grade_point': grade_point,
                'description': f'{grade} ({grade_point} GPA)'
            })
        except ValueError:
            return JsonResponse({'error': 'Invalid marks'}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


# API ViewSets
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsTeacherOrAdmin]
        elif self.action in ['create', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Student.objects.all()
        elif hasattr(user, 'teacher'):
            # Teachers can see students in their courses
            teacher_courses = Course.objects.filter(teacher=user.teacher)
            enrolled_students = Enrollment.objects.filter(course__in=teacher_courses).values_list('student', flat=True)
            return Student.objects.filter(id__in=enrolled_students)
        elif hasattr(user, 'student'):
            # Students can only see themselves
            return Student.objects.filter(user=user)
        return Student.objects.none()


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdmin]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsTeacherOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get students enrolled in a course"""
        course = self.get_object()
        enrollments = Enrollment.objects.filter(course=course)
        students = [enrollment.student for enrollment in enrollments]
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsTeacherOrAdmin]


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            permission_classes = [IsTeacherOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Attendance.objects.all()
        elif hasattr(user, 'teacher'):
            # Teachers can see attendance for their courses
            teacher_courses = Course.objects.filter(teacher=user.teacher)
            return Attendance.objects.filter(course__in=teacher_courses)
        elif hasattr(user, 'student'):
            # Students can only see their own attendance
            return Attendance.objects.filter(student=user.student)
        return Attendance.objects.none()


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            permission_classes = [IsTeacherOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Grade.objects.all()
        elif hasattr(user, 'teacher'):
            # Teachers can see grades for their courses
            teacher_courses = Course.objects.filter(teacher=user.teacher)
            return Grade.objects.filter(course__in=teacher_courses)
        elif hasattr(user, 'student'):
            # Students can only see their own grades
            return Grade.objects.filter(student=user.student)
        return Grade.objects.none()
