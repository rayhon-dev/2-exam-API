from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from core.permissions import IsCourseTeacherOrAdmin, IsTeacher, IsEnrolledOrTeacherOrAdmin
from .models import Category, Course, Lesson, Module
from .serializers import CategorySerializer, CourseSerializer, LessonSerializer, ModuleSerializer
from .pagination import CoursePagination, CategoryPagination, LessonPagination, ModulePagination
from rest_framework.decorators import action
from rest_framework.response import Response


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CoursePagination

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [IsCourseTeacherOrAdmin()]
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action == 'category':
            return [AllowAny()]
        return [IsTeacher()]


    @action(detail=False, methods=['get'], url_path='category/(?P<category_id>[^/.]+)')
    def category(self, request, category_id=None):
        courses = Course.objects.filter(category_id=category_id)
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)



class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    pagination_class = ModulePagination

    def get_permissions(self):
        if self.action in ['create','update', 'destroy']:
            return [IsCourseTeacherOrAdmin()]

        return [IsAuthenticated()]

    @action(detail=False, methods=['get'], url_path='course/(?P<course_id>[^/.]+)')
    def category(self, request, course_id=None):
        modules = Module.objects.filter(course_id=course_id)
        serializer = self.get_serializer(modules, many=True)
        return Response(serializer.data)



class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPagination


    def get_permissions(self):
        if self.action in ['retrieve']:
            return [IsEnrolledOrTeacherOrAdmin()]

        if self.action in ['create', 'update', 'destroy']:
            return [IsCourseTeacherOrAdmin()]

        return [IsAuthenticated()]

    @action(detail=False, methods=['get'], url_path='module/(?P<module_id>[^/.]+)')
    def category(self, request, module_id=None):
        lessons = Lesson.objects.filter(module_id=module_id)
        serializer = self.get_serializer(lessons, many=True)
        return Response(serializer.data)