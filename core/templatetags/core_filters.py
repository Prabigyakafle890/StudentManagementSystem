from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using a key"""
    return dictionary.get(key)

@register.filter
def get_grade_marks(existing_grades, student_id):
    """Get marks for a student from existing grades"""
    grade = existing_grades.get(student_id)
    return grade.marks if grade else ''

@register.filter
def get_grade_letter(existing_grades, student_id):
    """Get grade letter for a student from existing grades"""
    grade = existing_grades.get(student_id)
    return grade.grade if grade else ''