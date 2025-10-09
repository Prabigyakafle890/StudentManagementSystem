
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	email = models.EmailField(unique=True)
	roll_no = models.CharField(max_length=20, unique=True)
	student_class = models.CharField(max_length=20)
	date_of_birth = models.DateField()
	gender = models.CharField(max_length=10)

	def __str__(self):
		return f"{self.name} ({self.roll_no})"
	
	@property
	def gpa(self):
		"""Calculate student's overall GPA"""
		from core.utils.grading import calculate_student_gpa
		return calculate_student_gpa(self)

class Teacher(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	subject = models.CharField(max_length=100)
	email = models.EmailField(unique=True)
	phone = models.CharField(max_length=20)

	def __str__(self):
		return self.name

class Course(models.Model):
	name = models.CharField(max_length=100)
	code = models.CharField(max_length=20, unique=True)
	description = models.TextField()
	teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return f"{self.name} ({self.code})"

class Enrollment(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	date_joined = models.DateField(auto_now_add=True)

	class Meta:
		unique_together = ('student', 'course')

	def __str__(self):
		return f"{self.student} enrolled in {self.course}"

class Attendance(models.Model):
	STATUS_CHOICES = (
		('Present', 'Present'),
		('Absent', 'Absent'),
	)
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	date = models.DateField()
	status = models.CharField(max_length=10, choices=STATUS_CHOICES)

	class Meta:
		unique_together = ('student', 'course', 'date')

	def __str__(self):
		return f"{self.student} - {self.course} on {self.date}: {self.status}"

class Grade(models.Model):
	GRADE_CHOICES = [
		('A+', 'A+ (Outstanding)'),
		('A', 'A (Excellent)'),
		('B+', 'B+ (Very Good)'),
		('B', 'B (Good)'),
		('C+', 'C+ (Satisfactory)'),
		('C', 'C (Acceptable)'),
		('D+', 'D+ (Needs Improvement)'),
		('D', 'D (Minimal)'),
		('E', 'E (Insufficient)'),
	]
	
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	marks = models.FloatField()
	grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
	grade_point = models.FloatField(default=0.0)  # GPA point for this grade

	class Meta:
		unique_together = ('student', 'course')

	def save(self, *args, **kwargs):
		# Automatically calculate grade and grade point based on marks
		from core.utils.grading import calculate_nepali_grade
		self.grade, self.grade_point = calculate_nepali_grade(self.marks)
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.student} - {self.course}: {self.grade} ({self.marks}%)"
