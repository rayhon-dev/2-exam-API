from django.contrib import admin
from .models import Category, Course, Module, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'category', 'price', 'is_published', 'created_at')
    search_fields = ('title', 'description', 'teacher__username')
    list_filter = ('category', 'is_published')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'created_at')
    search_fields = ('title', 'course__title')
    list_filter = ('course',)
    readonly_fields = ('created_at',)
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order', 'duration', 'created_at')
    search_fields = ('title', 'module__title')
    list_filter = ('module',)
    readonly_fields = ('created_at', 'updated_at')
