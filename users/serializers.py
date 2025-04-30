from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_teacher = serializers.BooleanField()
    date_joined = serializers.DateTimeField(read_only=True)


    def create(self, validation_data):
        return User.objects.create_user(**validation_data)

