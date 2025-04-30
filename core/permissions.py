from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsCourseTeacherOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_staff or request.user.is_superuser:
            return True

        return obj.teacher == request.user


from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated and request.user.is_teacher

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.teacher == request.user
