from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Teacher, Student

class Command(BaseCommand):
    help = 'Update Student and Teacher model names to Nepali equivalents'

    def handle(self, *args, **options):
        self.stdout.write('Updating Student and Teacher model names to Nepali...')
        
        # Mapping from new usernames to full Nepali names
        teacher_names = {
            'ram_math': 'Ram Bahadur Sharma',
            'sita_eng': 'Sita Devi Poudel',
            'arjun_sci': 'Arjun Khatri',
            'maya_art': 'Maya Gurung',
            'vikram_pe': 'Vikram Tamang',
            'sunita_hist': 'Sunita Neupane',
            'kumar_music': 'Kumar Magar',
            'anita_lang': 'Anita Thapa',
        }
        
        student_names = {
            'priya_001': 'Priya Shrestha',
            'amit_002': 'Amit Gupta',
            'sarita_003': 'Sarita Rai',
            'raj_004': 'Raj Lama',
            'kavita_005': 'Kavita Bhatta',
            'suresh_006': 'Suresh Joshi',
            'dipti_007': 'Dipti Tiwari',
            'santosh_008': 'Santosh Adhikari',
            'rupa_009': 'Rupa Karki',
            'dinesh_010': 'Dinesh Basnet',
        }
        
        # Update Teachers
        self.stdout.write('Updating teacher names...')
        for username, full_name in teacher_names.items():
            try:
                user = User.objects.get(username=username)
                teacher = Teacher.objects.get(user=user)
                teacher.name = full_name
                teacher.save()
                self.stdout.write(f'✓ Updated teacher: {username} → {full_name}')
            except User.DoesNotExist:
                self.stdout.write(f'✗ User {username} not found')
            except Teacher.DoesNotExist:
                self.stdout.write(f'✗ Teacher profile not found for {username}')
        
        # Update Students
        self.stdout.write('Updating student names...')
        for username, full_name in student_names.items():
            try:
                user = User.objects.get(username=username)
                student = Student.objects.get(user=user)
                student.name = full_name
                student.save()
                self.stdout.write(f'✓ Updated student: {username} → {full_name}')
            except User.DoesNotExist:
                self.stdout.write(f'✗ User {username} not found')
            except Student.DoesNotExist:
                self.stdout.write(f'✗ Student profile not found for {username}')
        
        self.stdout.write(self.style.SUCCESS('Successfully updated all Student and Teacher model names to Nepali!'))