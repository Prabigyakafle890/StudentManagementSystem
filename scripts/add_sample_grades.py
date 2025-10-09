#!/usr/bin/env python
"""
Add sample grades to the database
"""
import os
import sys
import django
from random import uniform, choice

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sms.settings')
django.setup()

from core.models import Student, Course, Grade, Enrollment

def add_sample_grades():
    """Add sample grades for enrolled students"""
    
    # Get all enrollments
    enrollments = Enrollment.objects.all()
    
    grades_added = 0
    
    for enrollment in enrollments:
        # Skip if grade already exists
        if Grade.objects.filter(student=enrollment.student, course=enrollment.course).exists():
            continue
            
        # Generate random marks between 50-100
        marks = round(uniform(50, 100), 1)
        
        # Calculate grade based on marks
        if marks >= 95: grade = 'A+'
        elif marks >= 90: grade = 'A'
        elif marks >= 85: grade = 'A-'
        elif marks >= 80: grade = 'B+'
        elif marks >= 75: grade = 'B'
        elif marks >= 70: grade = 'B-'
        elif marks >= 65: grade = 'C+'
        elif marks >= 60: grade = 'C'
        elif marks >= 55: grade = 'C-'
        elif marks >= 50: grade = 'D'
        else: grade = 'F'
        
        # Create grade
        Grade.objects.create(
            student=enrollment.student,
            course=enrollment.course,
            marks=marks,
            grade=grade
        )
        
        grades_added += 1
        print(f"Added grade for {enrollment.student.name} in {enrollment.course.name}: {marks}% ({grade})")
    
    print(f"\n✅ Successfully added {grades_added} sample grades!")
    print(f"📊 Total grades in database: {Grade.objects.count()}")

if __name__ == '__main__':
    add_sample_grades()