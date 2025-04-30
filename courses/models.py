from django.db import models

from core.base_models import BaseModel
from users.models import User


class Category(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Course(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='course_images/')
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Module(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(BaseModel):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField()
    video_url = models.URLField(null=True, blank=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.module.title} - {self.title}"
