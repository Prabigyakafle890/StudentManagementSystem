from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student, Teacher, Course, Enrollment, Attendance, Grade


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'user', 'name', 'email', 'roll_no', 'student_class', 'date_of_birth', 'gender']


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Teacher
        fields = ['id', 'user', 'name', 'subject', 'email', 'phone']


class CourseSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)
    teacher_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'description', 'teacher', 'teacher_id']


class EnrollmentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    course_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'date_joined', 'student_id', 'course_id']


class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    course_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'course', 'date', 'status', 'student_id', 'course_id']


class GradeSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    course_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Grade
        fields = ['id', 'student', 'course', 'marks', 'grade', 'grade_point', 'student_id', 'course_id']