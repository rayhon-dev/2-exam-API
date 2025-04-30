from rest_framework import serializers
from .models import Enrollment, Progress
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class CourseSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title']

class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseSimpleSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        source='course', queryset=Course.objects.all(), write_only=True
    )

    class Meta:
        model = Enrollment
        fields = [
            'id',
            'user',
            'course',
            'course_id',
            'enrolled_at',
            'is_completed',
            'completed_at'
        ]
        read_only_fields = ['id', 'user', 'course', 'enrolled_at', 'is_completed', 'completed_at']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class EnrollmentSimpleSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = ['id', 'course']

    def get_course(self, obj):
        return {
            "id": obj.course.id,
            "title": obj.course.title
        }


class LessonSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title']


class ProgressSerializer(serializers.ModelSerializer):
    enrollment = EnrollmentSimpleSerializer(read_only=True)
    lesson = LessonSimpleSerializer(read_only=True)
    enrollment_id = serializers.PrimaryKeyRelatedField(
        source='enrollment', queryset=Enrollment.objects.all(), write_only=True
    )
    lesson_id = serializers.PrimaryKeyRelatedField(
        source='lesson', queryset=Lesson.objects.all(), write_only=True
    )

    class Meta:
        model = Progress
        fields = [
            'id',
            'enrollment',
            'enrollment_id',
            'lesson',
            'lesson_id',
            'is_completed',
            'completed_at'
        ]
        read_only_fields = ['id', 'enrollment', 'lesson', 'completed_at']