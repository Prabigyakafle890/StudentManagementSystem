from rest_framework import permissions
from django.contrib.auth.models import User, Group


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins to access certain views.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsTeacher(permissions.BasePermission):
    """
    Custom permission to only allow teachers to access certain views.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return hasattr(request.user, 'teacher')


class IsStudent(permissions.BasePermission):
    """
    Custom permission to only allow students to access certain views.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return hasattr(request.user, 'student')


class IsTeacherOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow teachers and admins.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_staff or hasattr(request.user, 'teacher')


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        # For student objects, only the student themselves can access
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # For other objects linked to students/teachers
        if hasattr(obj, 'student') and hasattr(request.user, 'student'):
            return obj.student == request.user.student
        
        if hasattr(obj, 'teacher') and hasattr(request.user, 'teacher'):
            return obj.teacher == request.user.teacher
            
        return False