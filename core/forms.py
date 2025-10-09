from django import forms
from django.contrib.auth.models import User
from .models import Student, Teacher, Course, Enrollment, Attendance, Grade


class GradeEntryForm(forms.ModelForm):
    """Form for entering/updating student grades"""
    
    class Meta:
        model = Grade
        fields = ['student', 'course', 'marks', 'grade']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'marks': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'step': 0.1,
                'placeholder': 'Enter marks (0-100)'
            }),
            'grade': forms.Select(attrs={'class': 'form-select'})
        }
    
    GRADE_CHOICES = [
        ('A+', 'A+ (95-100)'),
        ('A', 'A (90-94)'),
        ('A-', 'A- (85-89)'),
        ('B+', 'B+ (80-84)'),
        ('B', 'B (75-79)'),
        ('B-', 'B- (70-74)'),
        ('C+', 'C+ (65-69)'),
        ('C', 'C (60-64)'),
        ('C-', 'C- (55-59)'),
        ('D', 'D (50-54)'),
        ('F', 'F (0-49)')
    ]
    
    grade = forms.ChoiceField(choices=GRADE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        
        if teacher:
            # Limit courses to those taught by this teacher
            teacher_courses = Course.objects.filter(teacher=teacher)
            self.fields['course'].queryset = teacher_courses
            
            # Limit students to those enrolled in teacher's courses
            enrolled_students = Student.objects.filter(
                enrollment__course__in=teacher_courses
            ).distinct()
            self.fields['student'].queryset = enrolled_students
        
        # Auto-calculate grade based on marks
        if 'marks' in self.data:
            try:
                marks = float(self.data['marks'])
                self.fields['grade'].initial = self.calculate_grade(marks)
            except (ValueError, TypeError):
                pass
    
    def calculate_grade(self, marks):
        """Calculate letter grade based on marks"""
        if marks >= 95: return 'A+'
        elif marks >= 90: return 'A'
        elif marks >= 85: return 'A-'
        elif marks >= 80: return 'B+'
        elif marks >= 75: return 'B'
        elif marks >= 70: return 'B-'
        elif marks >= 65: return 'C+'
        elif marks >= 60: return 'C'
        elif marks >= 55: return 'C-'
        elif marks >= 50: return 'D'
        else: return 'F'
    
    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        course = cleaned_data.get('course')
        marks = cleaned_data.get('marks')
        
        # Check if student is enrolled in the course
        if student and course:
            if not Enrollment.objects.filter(student=student, course=course).exists():
                raise forms.ValidationError(
                    f"{student.name} is not enrolled in {course.name}. "
                    "Only enrolled students can receive grades."
                )
        
        # Auto-calculate grade if marks provided
        if marks is not None:
            cleaned_data['grade'] = self.calculate_grade(marks)
        
        return cleaned_data


class BulkGradeEntryForm(forms.Form):
    """Form for entering grades for multiple students in a course"""
    
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select a course"
    )
    
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        
        if teacher:
            # Limit courses to those taught by this teacher
            self.fields['course'].queryset = Course.objects.filter(teacher=teacher)


class AttendanceEntryForm(forms.ModelForm):
    """Form for marking attendance"""
    
    class Meta:
        model = Attendance
        fields = ['student', 'course', 'date', 'status']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={'class': 'form-select'})
        }
    
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        
        if teacher:
            # Limit courses to those taught by this teacher
            teacher_courses = Course.objects.filter(teacher=teacher)
            self.fields['course'].queryset = teacher_courses
            
            # Limit students to those enrolled in teacher's courses
            enrolled_students = Student.objects.filter(
                enrollment__course__in=teacher_courses
            ).distinct()
            self.fields['student'].queryset = enrolled_students


class BulkAttendanceForm(forms.Form):
    """Form for marking attendance for multiple students"""
    
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select a course"
    )
    
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        
        if teacher:
            self.fields['course'].queryset = Course.objects.filter(teacher=teacher)