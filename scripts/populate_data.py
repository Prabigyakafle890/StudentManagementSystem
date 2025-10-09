from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Student, Teacher, Course, Enrollment, Attendance, Grade
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data population...'))

        # Create sample teachers
        teacher_data = [
            {'username': 'john_math', 'first_name': 'John', 'last_name': 'Smith', 'email': 'john@school.edu', 'subject': 'Mathematics', 'phone': '555-0101'},
            {'username': 'sarah_eng', 'first_name': 'Sarah', 'last_name': 'Johnson', 'email': 'sarah@school.edu', 'subject': 'English', 'phone': '555-0102'},
            {'username': 'mike_sci', 'first_name': 'Mike', 'last_name': 'Wilson', 'email': 'mike@school.edu', 'subject': 'Science', 'phone': '555-0103'},
        ]

        teachers = []
        for data in teacher_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': data['email'],
                    'is_staff': False
                }
            )
            if created:
                user.set_password('teacher123')
                user.save()

            teacher, created = Teacher.objects.get_or_create(
                user=user,
                defaults={
                    'name': f"{data['first_name']} {data['last_name']}",
                    'subject': data['subject'],
                    'email': data['email'],
                    'phone': data['phone']
                }
            )
            teachers.append(teacher)
            if created:
                self.stdout.write(f'Created teacher: {teacher.name}')

        # Create sample students
        student_data = [
            {'username': 'alice_001', 'first_name': 'Alice', 'last_name': 'Brown', 'email': 'alice@student.edu', 'roll_no': 'STU001', 'class': '10A', 'dob': '2008-05-15', 'gender': 'Female'},
            {'username': 'bob_002', 'first_name': 'Bob', 'last_name': 'Davis', 'email': 'bob@student.edu', 'roll_no': 'STU002', 'class': '10A', 'dob': '2008-03-22', 'gender': 'Male'},
            {'username': 'carol_003', 'first_name': 'Carol', 'last_name': 'Miller', 'email': 'carol@student.edu', 'roll_no': 'STU003', 'class': '10B', 'dob': '2008-07-08', 'gender': 'Female'},
            {'username': 'david_004', 'first_name': 'David', 'last_name': 'Garcia', 'email': 'david@student.edu', 'roll_no': 'STU004', 'class': '10B', 'dob': '2008-01-12', 'gender': 'Male'},
            {'username': 'eve_005', 'first_name': 'Eve', 'last_name': 'Martinez', 'email': 'eve@student.edu', 'roll_no': 'STU005', 'class': '10A', 'dob': '2008-09-30', 'gender': 'Female'},
        ]

        students = []
        for data in student_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': data['email'],
                    'is_staff': False
                }
            )
            if created:
                user.set_password('student123')
                user.save()

            student, created = Student.objects.get_or_create(
                user=user,
                defaults={
                    'name': f"{data['first_name']} {data['last_name']}",
                    'email': data['email'],
                    'roll_no': data['roll_no'],
                    'student_class': data['class'],
                    'date_of_birth': data['dob'],
                    'gender': data['gender']
                }
            )
            students.append(student)
            if created:
                self.stdout.write(f'Created student: {student.name}')

        # Create sample courses
        course_data = [
            {'name': 'Advanced Mathematics', 'code': 'MATH101', 'description': 'Advanced mathematical concepts for grade 10', 'teacher': teachers[0]},
            {'name': 'English Literature', 'code': 'ENG101', 'description': 'Classic and modern literature analysis', 'teacher': teachers[1]},
            {'name': 'General Science', 'code': 'SCI101', 'description': 'Introduction to physics, chemistry, and biology', 'teacher': teachers[2]},
        ]

        courses = []
        for data in course_data:
            course, created = Course.objects.get_or_create(
                code=data['code'],
                defaults={
                    'name': data['name'],
                    'description': data['description'],
                    'teacher': data['teacher']
                }
            )
            courses.append(course)
            if created:
                self.stdout.write(f'Created course: {course.name}')

        # Create enrollments
        for student in students:
            for course in courses:
                enrollment, created = Enrollment.objects.get_or_create(
                    student=student,
                    course=course
                )
                if created:
                    self.stdout.write(f'Enrolled {student.name} in {course.name}')

        # Create sample attendance records (last 30 days)
        for i in range(30):
            attendance_date = date.today() - timedelta(days=i)
            for student in students:
                for course in courses:
                    # Random attendance (90% present)
                    status = 'Present' if random.random() > 0.1 else 'Absent'
                    attendance, created = Attendance.objects.get_or_create(
                        student=student,
                        course=course,
                        date=attendance_date,
                        defaults={'status': status}
                    )

        # Create sample grades
        grade_scale = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F']
        marks_range = [(95, 'A+'), (90, 'A'), (85, 'A-'), (80, 'B+'), (75, 'B'), 
                      (70, 'B-'), (65, 'C+'), (60, 'C'), (55, 'C-'), (50, 'D'), (0, 'F')]

        for student in students:
            for course in courses:
                # Random marks between 50-100
                marks = random.randint(50, 100)
                grade = next(g for m, g in marks_range if marks >= m)
                
                grade_obj, created = Grade.objects.get_or_create(
                    student=student,
                    course=course,
                    defaults={
                        'marks': marks,
                        'grade': grade
                    }
                )
                if created:
                    self.stdout.write(f'Created grade for {student.name} in {course.name}: {grade}')

        self.stdout.write(self.style.SUCCESS('Sample data population completed!'))
        self.stdout.write(self.style.WARNING('Teacher login: username="john_math", password="teacher123"'))
        self.stdout.write(self.style.WARNING('Student login: username="alice_001", password="student123"'))