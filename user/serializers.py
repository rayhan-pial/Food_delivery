from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role', 'is_active']
        extra_kwargs = {
            'email': {'required': True},
            'role': {'required': True},
            'name': {'required': True},
            'id': {'read_only': True},
        }


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

