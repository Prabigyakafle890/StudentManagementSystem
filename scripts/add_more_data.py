from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Student, Teacher, Course, Enrollment, Attendance, Grade
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Add more courses, teachers, and students to the database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Adding more data to the system...'))

        # Additional teachers
        additional_teachers = [
            {'username': 'emily_art', 'first_name': 'Emily', 'last_name': 'Chen', 'email': 'emily@school.edu', 'subject': 'Art', 'phone': '555-0104'},
            {'username': 'david_pe', 'first_name': 'David', 'last_name': 'Rodriguez', 'email': 'david@school.edu', 'subject': 'Physical Education', 'phone': '555-0105'},
            {'username': 'lisa_hist', 'first_name': 'Lisa', 'last_name': 'Thompson', 'email': 'lisa@school.edu', 'subject': 'History', 'phone': '555-0106'},
            {'username': 'mark_music', 'first_name': 'Mark', 'last_name': 'Anderson', 'email': 'mark@school.edu', 'subject': 'Music', 'phone': '555-0107'},
            {'username': 'anna_lang', 'first_name': 'Anna', 'last_name': 'Williams', 'email': 'anna@school.edu', 'subject': 'Foreign Languages', 'phone': '555-0108'},
        ]

        teachers = []
        for data in additional_teachers:
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

        # Additional students
        additional_students = [
            {'username': 'frank_006', 'first_name': 'Frank', 'last_name': 'Wilson', 'email': 'frank@student.edu', 'roll_no': 'STU006', 'class': '10C', 'dob': '2008-02-14', 'gender': 'Male'},
            {'username': 'grace_007', 'first_name': 'Grace', 'last_name': 'Lee', 'email': 'grace@student.edu', 'roll_no': 'STU007', 'class': '10C', 'dob': '2008-11-20', 'gender': 'Female'},
            {'username': 'henry_008', 'first_name': 'Henry', 'last_name': 'Taylor', 'email': 'henry@student.edu', 'roll_no': 'STU008', 'class': '11A', 'dob': '2007-04-10', 'gender': 'Male'},
            {'username': 'iris_009', 'first_name': 'Iris', 'last_name': 'Clark', 'email': 'iris@student.edu', 'roll_no': 'STU009', 'class': '11A', 'dob': '2007-08-15', 'gender': 'Female'},
            {'username': 'jack_010', 'first_name': 'Jack', 'last_name': 'Moore', 'email': 'jack@student.edu', 'roll_no': 'STU010', 'class': '11B', 'dob': '2007-06-25', 'gender': 'Male'},
        ]

        students = []
        for data in additional_students:
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

        # Additional courses
        all_teachers = Teacher.objects.all()
        additional_courses = [
            {'name': 'Creative Arts', 'code': 'ART101', 'description': 'Introduction to visual arts and creativity', 'subject': 'Art'},
            {'name': 'Physical Education', 'code': 'PE101', 'description': 'Sports, fitness, and healthy lifestyle', 'subject': 'Physical Education'},
            {'name': 'World History', 'code': 'HIST101', 'description': 'Ancient civilizations to modern times', 'subject': 'History'},
            {'name': 'Music Theory', 'code': 'MUS101', 'description': 'Basic music theory and appreciation', 'subject': 'Music'},
            {'name': 'Spanish Language', 'code': 'SPAN101', 'description': 'Introduction to Spanish language and culture', 'subject': 'Foreign Languages'},
            {'name': 'Advanced Mathematics', 'code': 'MATH201', 'description': 'Calculus and advanced mathematical concepts', 'subject': 'Mathematics'},
            {'name': 'Biology', 'code': 'BIO101', 'description': 'Life sciences and biological processes', 'subject': 'Science'},
            {'name': 'Computer Science', 'code': 'CS101', 'description': 'Programming fundamentals and computer literacy', 'subject': 'Mathematics'},
        ]

        courses = []
        for data in additional_courses:
            # Find teacher by subject
            teacher = all_teachers.filter(subject=data['subject']).first()
            
            course, created = Course.objects.get_or_create(
                code=data['code'],
                defaults={
                    'name': data['name'],
                    'description': data['description'],
                    'teacher': teacher
                }
            )
            courses.append(course)
            if created:
                self.stdout.write(f'Created course: {course.name} assigned to {teacher.name if teacher else "No teacher"}')

        # Enroll all students in some courses
        all_students = Student.objects.all()
        all_courses = Course.objects.all()
        
        for student in all_students:
            # Randomly enroll each student in 4-6 courses
            student_courses = random.sample(list(all_courses), random.randint(4, min(6, len(all_courses))))
            for course in student_courses:
                enrollment, created = Enrollment.objects.get_or_create(
                    student=student,
                    course=course
                )

        # Generate more attendance records
        for i in range(60):  # 60 days of attendance
            attendance_date = date.today() - timedelta(days=i)
            for student in all_students:
                enrolled_courses = Course.objects.filter(enrollment__student=student)
                for course in enrolled_courses:
                    # 85% attendance rate
                    status = 'Present' if random.random() > 0.15 else 'Absent'
                    attendance, created = Attendance.objects.get_or_create(
                        student=student,
                        course=course,
                        date=attendance_date,
                        defaults={'status': status}
                    )

        # Generate grades for all enrolled students
        grade_options = [
            (95, 'A+'), (92, 'A'), (88, 'A-'), (85, 'B+'), (82, 'B'), 
            (78, 'B-'), (75, 'C+'), (72, 'C'), (68, 'C-'), (65, 'D'), (50, 'F')
        ]

        for student in all_students:
            enrolled_courses = Course.objects.filter(enrollment__student=student)
            for course in enrolled_courses:
                # Generate random but realistic grades
                marks, grade_letter = random.choice(grade_options)
                marks += random.randint(-5, 5)  # Add some variation
                marks = max(0, min(100, marks))  # Keep within 0-100 range
                
                # Determine grade based on marks
                if marks >= 95: grade_letter = 'A+'
                elif marks >= 90: grade_letter = 'A'
                elif marks >= 85: grade_letter = 'A-'
                elif marks >= 80: grade_letter = 'B+'
                elif marks >= 75: grade_letter = 'B'
                elif marks >= 70: grade_letter = 'B-'
                elif marks >= 65: grade_letter = 'C+'
                elif marks >= 60: grade_letter = 'C'
                elif marks >= 55: grade_letter = 'C-'
                elif marks >= 50: grade_letter = 'D'
                else: grade_letter = 'F'
                
                grade_obj, created = Grade.objects.get_or_create(
                    student=student,
                    course=course,
                    defaults={
                        'marks': marks,
                        'grade': grade_letter
                    }
                )

        self.stdout.write(self.style.SUCCESS('Enhanced data population completed!'))
        self.stdout.write(self.style.WARNING(f'Total Teachers: {Teacher.objects.count()}'))
        self.stdout.write(self.style.WARNING(f'Total Students: {Student.objects.count()}'))
        self.stdout.write(self.style.WARNING(f'Total Courses: {Course.objects.count()}'))
        self.stdout.write(self.style.WARNING(f'Total Enrollments: {Enrollment.objects.count()}'))
        self.stdout.write(self.style.WARNING('Try logging in with any teacher (password: teacher123) or student (password: student123)!'))