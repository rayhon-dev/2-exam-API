from rest_framework.permissions import SAFE_METHODS, BasePermission
from enrollments.models import Enrollment


class IsCourseTeacherOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_staff or request.user.is_superuser:
            return True

        return obj.course.teacher == request.user



class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated and request.user.is_teacher
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        teacher = getattr(obj, 'teacher', None)
        if teacher is None and hasattr(obj, 'course'):
            teacher = getattr(obj.course, 'teacher', None)

        return teacher == request.user


class IsEnrolledOrTeacherOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_staff or user.is_superuser:
            return True

        if hasattr(obj, 'teacher') and obj.teacher == user:
            return True

        if hasattr(obj, 'id'):
            return Enrollment.objects.filter(user=user, course=obj).exists()

        return False


class IsEnrollmentOwnerOrTeacherOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_staff or user.is_superuser:
            return True

        if obj.user == user:
            return True

        if hasattr(obj, 'course') and obj.course.teacher == user:
            return True

        return False


class IsEnrollmentOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_staff or user.is_superuser:
            return True

        if obj.user == user:
            return True

        return False


class IsOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_staff or user.is_superuser:
            return True

        return getattr(obj, 'user', None) == user



class IsEnrollmentOwner(BasePermission):
    def has_object_permission(self, request, view, obj):

        return obj.user == request.user


class IsProgressOwnerOrTeacherOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.enrollment.user == request.user:
            return True

        if request.user.is_teacher and obj.enrollment.course.teacher == request.user:
            return True

        if request.user.is_staff:
            return True

        return False


class IsProgressOwner(BasePermission):
    def has_object_permission(self, request, view, obj):

        return obj.enrollment.user == request.user


class IsEnrolledAndCompleted(BasePermission):

    def has_permission(self, request, view):
        course_id = request.data.get('course') or request.data.get('course_id')
        if not course_id:
            return False

        return Enrollment.objects.filter(
            user=request.user,
            course_id=course_id,
            completed=True
        ).exists()


class IsReviewOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user



class IsReviewOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff