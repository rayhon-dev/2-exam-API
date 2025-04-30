from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CategoryViewSet, CourseViewSet, LessonViewSet, ModuleViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'modules', ModuleViewSet, basename='module')

urlpatterns = [
    path('', include(router.urls)),
]
