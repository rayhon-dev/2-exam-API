from rest_framework import serializers
from .models import Category, Course, Lesson, Module


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
            'icon',
            'created_at',
        ]


class LessonSerializer(serializers.ModelSerializer):
    module = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            'id',
            'title',
            'content',
            'video_url',
            'duration',
            'order',
            'module'
        ]

        extra_kwargs = {
            'id': {'read_only': True}
        }

    def get_module(self, obj):
        return {
            'id': obj.module.id,
            'title': obj.module.title
        }


class ModuleSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Module
        fields = [
            'id',
            'title',
            'description',
            'order',
            'course',
            'created_at',
            'lessons'
        ]

        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True}
        }

    def get_course(self, obj):
        return {
            'id': obj.course.id,
            'title': obj.course.title
        }

class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True)
    teacher = serializers.SerializerMethodField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'teacher',
            'category',
            'price',
            'discount_price',
            'image',
            'is_published',
            'created_at',
            'updated_at',
            'modules'
        ]
        read_only_fields = ['id', 'teacher', 'created_at', 'updated_at']

    def get_teacher(self, obj):
        return {
            'id': obj.teacher.id,
            'username': obj.teacher.username,
            'first_name': obj.teacher.first_name,
            'last_name': obj.teacher.last_name
        }

    def create(self, validated_data):
        modules_data = validated_data.pop('modules')
        course = Course.objects.create(**validated_data)
        for module_data in modules_data:
            lessons_data = module_data.pop('lessons')
            module = Module.objects.create(course=course, **module_data)
            for lesson_data in lessons_data:
                Lesson.objects.create(module=module, **lesson_data)
        return course
