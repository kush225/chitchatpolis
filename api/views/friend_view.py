from rest_framework import generics, status
from rest_framework.response import Response
from ..models import Friend, User
from ..serializers.friend_serializer import FriendSerializer
from rest_framework.permissions import IsAuthenticated
import logging
from django.db.models import Q

logger = logging.getLogger(__name__)

class ListFriendsAPI(generics.ListAPIView):
    """
    API endpoint for listing friends of the current user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FriendSerializer
    queryset = Friend.objects.all()

    def get_queryset(self):
        """
        Get the queryset of friends of the current user.
        """
        return self.queryset.filter(Q(user1=self.request.user) | Q(user2=self.request.user))
