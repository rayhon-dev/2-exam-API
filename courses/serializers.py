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
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True)
    course_info = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Module
        fields = [
            'id',
            'title',
            'description',
            'order',
            'course',  # for input (write_only)
            'course_info',  # for output (read_only)
            'created_at',
            'lessons'
        ]
        read_only_fields = ['id', 'created_at']

    def get_course_info(self, obj):
        return {
            'id': obj.course.id,
            'title': obj.course.title
        }

    def create(self, validated_data):
        lessons_data = validated_data.pop('lessons')
        course = validated_data.pop('course')
        module = Module.objects.create(course=course, **validated_data)

        for lesson_data in lessons_data:
            Lesson.objects.create(module=module, **lesson_data)

        return module

    def update(self, instance, validated_data):
        lessons_data = validated_data.pop('lessons', None)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.order = validated_data.get('order', instance.order)
        instance.save()

        if lessons_data is not None:
            instance.lessons.all().delete()  # eski lessonlar o‘chadi
            for lesson_data in lessons_data:
                Lesson.objects.create(module=instance, **lesson_data)

        return instance


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
        validated_data['teacher'] = self.context['request'].user

        course = Course.objects.create(**validated_data)

        for module_data in modules_data:
            lessons_data = module_data.pop('lessons')
            module = Module.objects.create(course=course, **module_data)
            for lesson_data in lessons_data:
                Lesson.objects.create(module=module, **lesson_data)

        return course

    def update(self, instance, validated_data):
        modules_data = validated_data.pop('modules', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        instance.modules.all().delete()

        for module_data in modules_data:
            lessons_data = module_data.pop('lessons', [])
            module = Module.objects.create(course=instance, **module_data)
            for lesson_data in lessons_data:
                Lesson.objects.create(module=module, **lesson_data)

        return instance
