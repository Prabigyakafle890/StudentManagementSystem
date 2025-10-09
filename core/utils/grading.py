# Nepali Grading System Utilities

def calculate_nepali_grade(marks):
    """
    Calculate grade based on Nepali grading system
    
    Grade Scale (based on Nepal's Higher Secondary Education):
    A+ = 90-100 (GPA: 4.0)
    A  = 80-89  (GPA: 3.6)
    B+ = 70-79  (GPA: 3.2)
    B  = 60-69  (GPA: 2.8)
    C+ = 50-59  (GPA: 2.4)
    C  = 40-49  (GPA: 2.0)
    D+ = 35-39  (GPA: 1.6)
    D  = 32-34  (GPA: 1.2)
    E  = 0-31   (GPA: 0.8)
    """
    if marks >= 90:
        return 'A+', 4.0
    elif marks >= 80:
        return 'A', 3.6
    elif marks >= 70:
        return 'B+', 3.2
    elif marks >= 60:
        return 'B', 2.8
    elif marks >= 50:
        return 'C+', 2.4
    elif marks >= 40:
        return 'C', 2.0
    elif marks >= 35:
        return 'D+', 1.6
    elif marks >= 32:
        return 'D', 1.2
    else:
        return 'E', 0.8

def get_grade_point(grade):
    """Get GPA point for a specific grade"""
    grade_points = {
        'A+': 4.0,
        'A': 3.6,
        'B+': 3.2,
        'B': 2.8,
        'C+': 2.4,
        'C': 2.0,
        'D+': 1.6,
        'D': 1.2,
        'E': 0.8
    }
    return grade_points.get(grade, 0.0)

def calculate_student_gpa(student):
    """Calculate overall GPA for a student based on all their grades"""
    from core.models import Grade
    
    grades = Grade.objects.filter(student=student)
    if not grades.exists():
        return 0.0
    
    total_points = sum(get_grade_point(grade.grade) for grade in grades)
    total_courses = grades.count()
    
    return round(total_points / total_courses, 2)

def get_grade_description(grade):
    """Get description for grade"""
    descriptions = {
        'A+': 'Outstanding',
        'A': 'Excellent',
        'B+': 'Very Good',
        'B': 'Good',
        'C+': 'Satisfactory',
        'C': 'Acceptable',
        'D+': 'Needs Improvement',
        'D': 'Minimal',
        'E': 'Insufficient'
    }
    return descriptions.get(grade, 'Unknown')