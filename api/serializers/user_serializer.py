from rest_framework import serializers
from typing import Any, Dict
from ..models import User
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'password')

    def create(self, validated_data: Dict[str, Any]) -> User:
        """
        Method to create a new user with validated data.
        """
        user = User.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
