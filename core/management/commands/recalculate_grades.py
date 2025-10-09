from django.core.management.base import BaseCommand
from core.models import Grade
from core.utils.grading import calculate_nepali_grade

class Command(BaseCommand):
    help = 'Recalculate all grades using Nepali grading system'

    def handle(self, *args, **options):
        self.stdout.write('Recalculating all grades using Nepali grading system...')
        
        grades = Grade.objects.all()
        updated_count = 0
        
        for grade in grades:
            old_grade = grade.grade
            old_points = getattr(grade, 'grade_point', 0.0)
            
            # Recalculate using Nepali system
            new_grade, new_points = calculate_nepali_grade(grade.marks)
            
            grade.grade = new_grade
            grade.grade_point = new_points
            grade.save()
            
            if old_grade != new_grade:
                self.stdout.write(
                    f'✓ {grade.student.name} - {grade.course.name}: '
                    f'{grade.marks}% → {old_grade} → {new_grade} (GPA: {new_points})'
                )
            else:
                self.stdout.write(
                    f'• {grade.student.name} - {grade.course.name}: '
                    f'{grade.marks}% → {new_grade} (GPA: {new_points}) [unchanged]'
                )
            
            updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully recalculated {updated_count} grades using Nepali grading system!'
            )
        )
        
        # Show grade distribution
        self.stdout.write('\n=== GRADE DISTRIBUTION ===')
        grade_counts = {}
        for grade in Grade.objects.all():
            grade_counts[grade.grade] = grade_counts.get(grade.grade, 0) + 1
        
        for grade_letter in ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D+', 'D', 'E']:
            count = grade_counts.get(grade_letter, 0)
            if count > 0:
                self.stdout.write(f'{grade_letter}: {count} students')
        
        # Show some student GPAs
        self.stdout.write('\n=== SAMPLE STUDENT GPAs ===')
        from core.models import Student
        students = Student.objects.all()[:5]
        for student in students:
            self.stdout.write(f'{student.name}: GPA {student.gpa}')