from rest_framework import serializers
from .models import User


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



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_teacher',
            'bio',
            'profile_picture',
            'date_joined',
        ]
        read_only_fields = ('id', 'username', 'email', 'is_teacher', 'date_joined')