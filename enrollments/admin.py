from django.contrib import admin
from .models import Enrollment, Progress

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'is_completed', 'created_at', 'completed_at')
    search_fields = ('user__username', 'course__title')
    list_filter = ('is_completed', 'course')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'lesson', 'is_completed', 'completed_at')
    search_fields = ('enrollment__user__username', 'lesson__title')
    list_filter = ('is_completed',)
