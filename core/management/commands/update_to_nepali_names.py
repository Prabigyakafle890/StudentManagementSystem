from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Teacher, Student

class Command(BaseCommand):
    help = 'Update all usernames and names to Nepali equivalents'

    def handle(self, *args, **options):
        self.stdout.write('Starting update to Nepali names...')
        
        # Mapping from old usernames to new Nepali usernames and names
        teacher_mappings = {
            'john_math': {'username': 'ram_math', 'first_name': 'Ram Bahadur', 'last_name': 'Sharma', 'full_name': 'Ram Bahadur Sharma'},
            'sarah_eng': {'username': 'sita_eng', 'first_name': 'Sita Devi', 'last_name': 'Poudel', 'full_name': 'Sita Devi Poudel'},
            'mike_sci': {'username': 'arjun_sci', 'first_name': 'Arjun', 'last_name': 'Khatri', 'full_name': 'Arjun Khatri'},
            'emily_art': {'username': 'maya_art', 'first_name': 'Maya', 'last_name': 'Gurung', 'full_name': 'Maya Gurung'},
            'david_pe': {'username': 'vikram_pe', 'first_name': 'Vikram', 'last_name': 'Tamang', 'full_name': 'Vikram Tamang'},
            'lisa_hist': {'username': 'sunita_hist', 'first_name': 'Sunita', 'last_name': 'Neupane', 'full_name': 'Sunita Neupane'},
            'mark_music': {'username': 'kumar_music', 'first_name': 'Kumar', 'last_name': 'Magar', 'full_name': 'Kumar Magar'},
            'anna_lang': {'username': 'anita_lang', 'first_name': 'Anita', 'last_name': 'Thapa', 'full_name': 'Anita Thapa'},
        }
        
        student_mappings = {
            'alice_001': {'username': 'priya_001', 'first_name': 'Priya', 'last_name': 'Shrestha', 'full_name': 'Priya Shrestha'},
            'bob_002': {'username': 'amit_002', 'first_name': 'Amit', 'last_name': 'Gupta', 'full_name': 'Amit Gupta'},
            'carol_003': {'username': 'sarita_003', 'first_name': 'Sarita', 'last_name': 'Rai', 'full_name': 'Sarita Rai'},
            'david_004': {'username': 'raj_004', 'first_name': 'Raj', 'last_name': 'Lama', 'full_name': 'Raj Lama'},
            'eve_005': {'username': 'kavita_005', 'first_name': 'Kavita', 'last_name': 'Bhatta', 'full_name': 'Kavita Bhatta'},
            'frank_006': {'username': 'suresh_006', 'first_name': 'Suresh', 'last_name': 'Joshi', 'full_name': 'Suresh Joshi'},
            'grace_007': {'username': 'dipti_007', 'first_name': 'Dipti', 'last_name': 'Tiwari', 'full_name': 'Dipti Tiwari'},
            'henry_008': {'username': 'santosh_008', 'first_name': 'Santosh', 'last_name': 'Adhikari', 'full_name': 'Santosh Adhikari'},
            'iris_009': {'username': 'rupa_009', 'first_name': 'Rupa', 'last_name': 'Karki', 'full_name': 'Rupa Karki'},
            'jack_010': {'username': 'dinesh_010', 'first_name': 'Dinesh', 'last_name': 'Basnet', 'full_name': 'Dinesh Basnet'},
        }
        
        # Update Teachers
        self.stdout.write('Updating teachers...')
        for old_username, new_data in teacher_mappings.items():
            try:
                user = User.objects.get(username=old_username)
                user.username = new_data['username']
                user.first_name = new_data['first_name']
                user.last_name = new_data['last_name']
                user.save()
                
                # Update Teacher model if it exists
                try:
                    teacher = Teacher.objects.get(user=user)
                    teacher.name = new_data['full_name']  # Update the name field in Teacher model
                    teacher.save()
                    self.stdout.write(f'✓ Updated teacher: {old_username} → {new_data["username"]} ({new_data["full_name"]})')
                except Teacher.DoesNotExist:
                    self.stdout.write(f'⚠ Teacher profile not found for {old_username}')
                    
            except User.DoesNotExist:
                self.stdout.write(f'✗ User {old_username} not found')
        
        # Update Students
        self.stdout.write('Updating students...')
        for old_username, new_data in student_mappings.items():
            try:
                user = User.objects.get(username=old_username)
                user.username = new_data['username']
                user.first_name = new_data['first_name']
                user.last_name = new_data['last_name']
                user.save()
                
                # Update Student model if it exists
                try:
                    student = Student.objects.get(user=user)
                    student.name = new_data['full_name']  # Update the name field in Student model
                    student.save()
                    self.stdout.write(f'✓ Updated student: {old_username} → {new_data["username"]} ({new_data["full_name"]})')
                except Student.DoesNotExist:
                    self.stdout.write(f'⚠ Student profile not found for {old_username}')
                    
            except User.DoesNotExist:
                self.stdout.write(f'✗ User {old_username} not found')
        
        self.stdout.write(self.style.SUCCESS('Successfully updated all names to Nepali!'))
        self.stdout.write('You can now login with the new usernames like: ram_math, sita_eng, priya_001, sarita_003, etc.')