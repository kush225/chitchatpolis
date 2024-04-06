from rest_framework import serializers
from ..models import Friend
from typing import Any

class FriendSerializer(serializers.ModelSerializer):
    """
    Serializer for Friend model.
    """

    friend = serializers.SerializerMethodField()

    class Meta:
        model = Friend
        fields = ("id", "friend")

    def get_friend(self, obj: Friend) -> str:
        """
        Get the name of the friend based on the context user.
        """
        if obj.user1 == self.context["request"].user:
            return obj.user2.name
        else:
            return obj.user1.name
