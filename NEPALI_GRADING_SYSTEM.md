# EduManager - Nepali Grading System

## Grade Scale (Based on Nepal's Higher Secondary Education)

| Grade | Marks Range | GPA Points | Description |
|-------|-------------|------------|-------------|
| A+    | 90-100      | 4.0        | Outstanding |
| A     | 80-89       | 3.6        | Excellent   |
| B+    | 70-79       | 3.2        | Very Good   |
| B     | 60-69       | 2.8        | Good        |
| C+    | 50-59       | 2.4        | Satisfactory |
| C     | 40-49       | 2.0        | Acceptable  |
| D+    | 35-39       | 1.6        | Needs Improvement |
| D     | 32-34       | 1.2        | Minimal     |
| E     | 0-31        | 0.8        | Insufficient |

## Features

### Automatic Grade Calculation
- Grades are automatically calculated when marks are entered
- GPA points are assigned based on the Nepali scale
- No more American A-F system with minus grades

### GPA Calculation
- Each student has an overall GPA calculated from all courses
- GPA is the average of all grade points
- Displayed with 2 decimal places (e.g., 3.43)

### Updated Components

1. **Grade Model**: Now includes `grade_point` field and automatic calculation
2. **Student Model**: Added `gpa` property for easy access to overall GPA
3. **Grading Utilities**: New utility functions for grade calculation
4. **Views**: Updated to use Nepali grading system
5. **AJAX Endpoints**: Updated for real-time grade calculation

### Usage Examples

```python
# Create a new grade
from core.models import Grade, Student, Course
grade = Grade.objects.create(
    student=student,
    course=course,
    marks=85  # Automatically becomes 'A' with 3.6 GPA points
)

# Get student's overall GPA
student = Student.objects.get(roll_no='STU001')
print(f"GPA: {student.gpa}")  # e.g., "GPA: 3.43"
```

### Migration Applied
- Added `grade_point` field to Grade model
- Updated existing grades to new Nepali system
- All students now have accurate GPAs  

## Sample Grade Distribution After Update

- A+: 10 students (Outstanding)
- A: 18 students (Excellent)  
- B+: 10 students (Very Good)
- B: 9 students (Good)
- C+: 6 students (Satisfactory)
- C: 5 students (Acceptable)

Total: 58 grades recalculated successfully