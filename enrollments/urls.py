from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import EnrollmentViewSet, ProgressViewSet

router = DefaultRouter()
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'progress', ProgressViewSet, basename='progress')


urlpatterns = [
    path('', include(router.urls)),
]
