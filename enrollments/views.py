from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .pagination import EnrollmentPagination, ProgressPagination
from .serializers import EnrollmentSerializer, ProgressSerializer
from .models import Enrollment, Progress
from core.permissions import (
        IsEnrollmentOwnerOrTeacherOrAdmin,
        IsEnrollmentOwnerOrAdmin,
        IsOwnerOrAdmin,
        IsCourseTeacherOrAdmin,
        IsEnrollmentOwner,
        IsProgressOwner,
        IsProgressOwnerOrTeacherOrAdmin
)


class EnrollmentViewSet(ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    pagination_class = EnrollmentPagination

    def get_permissions(self):
        if self.action in ['retrieve', 'update']:
            return [IsEnrollmentOwnerOrTeacherOrAdmin()]
        elif self.action == 'list':
            return [IsAdminUser()]
        elif self.action == 'destroy':
            return [IsEnrollmentOwnerOrAdmin()]
        elif self.action == 'user_enrollments':
            return [IsOwnerOrAdmin()]
        elif self.action == 'course_enrollments':
            return [IsCourseTeacherOrAdmin()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)', name='user_enrollments')
    def user_enrollments(self, request, user_id=None):
        enrollments = Enrollment.objects.filter(user_id=user_id)
        self.check_object_permissions(request, enrollments.first())
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'], url_path='course/(?P<course_id>[^/.]+)', name='course_enrollments')
    def course_enrollments(self, request, course_id=None):
        enrollments = Enrollment.objects.filter(course_id=course_id)
        self.check_object_permissions(request, enrollments.first())
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)


class ProgressViewSet(ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    pagination_class = ProgressPagination


    def get_permissions(self):
        if self.action == 'list':
            return [IsAdminUser()]
        elif self.action == 'create':
            return [IsEnrollmentOwner()]
        elif self.action == 'retrieve':
            return [IsProgressOwnerOrTeacherOrAdmin()]
        elif self.action == 'update':
            return [IsProgressOwner()]
        elif self.action == 'enrollments_progress':
            return [IsEnrollmentOwnerOrTeacherOrAdmin()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'], url_path='enrollment/(?P<enrollment_id>[^/.]+)')
    def enrollments_progress(self, request, enrollment_id=None):
        progress = Progress.objects.filter(enrollment_id=enrollment_id)
        if not progress.exists():
            return Response({"detail": "No progress found."}, status=404)

        self.check_object_permissions(request, progress.first())
        serializer = self.get_serializer(progress, many=True)
        return Response(serializer.data)
