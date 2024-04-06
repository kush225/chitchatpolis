from rest_framework import serializers
from ..models import FriendRequest, User
from django.core.exceptions import ValidationError
from ..models.friend_request import STATUS_CHOICES

class FriendRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for FriendRequest model.
    """
    receiver_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='receiver', write_only=True)
    
    class Meta:
        model = FriendRequest
        fields = ('id', 'receiver_id', 'created_at', 'status')


class FriendRequestUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating FriendRequest status.
    """
    def validate_status(self, value: str) -> str:
        """
        Validates the status field.
        """
        if value not in (STATUS_CHOICES[0][0], STATUS_CHOICES[1][0]):
            raise ValidationError('Not acceptable status value')
        return value

    class Meta:
        model = FriendRequest
        fields = ('status',)
