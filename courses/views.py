from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Category, Course, Lesson, Module
from .serializers import CategorySerializer, CourseSerializer, LessonSerializer, ModuleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CategorySerializer
    