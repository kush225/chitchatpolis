from rest_framework import generics, status
from rest_framework.response import Response
from ..models import FriendRequest, User
from ..serializers.user_serializer import UserSerializer
from rest_framework.permissions import IsAuthenticated
import logging

logger = logging.getLogger(__name__)

class ListFriendsAPI(generics.ListAPIView):
    """
    API endpoint for listing friends of the current user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Get the queryset of friends for the current user.
        """
        user = self.request.user
        friends = FriendRequest.objects.filter(sender=user, status='accepted') | FriendRequest.objects.filter(receiver=user, status='accepted')
        friend_ids = []
        for friend in friends:
            if friend.sender == user:
                friend_ids.append(friend.receiver.id)
            else:
                friend_ids.append(friend.sender.id)
        return User.objects.filter(id__in=friend_ids)

    def list(self, request, *args, **kwargs):
        """
        List the friends of the current user.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        logger.info(f"List of friends returned for user: {request.user.email}")
        return Response(serializer.data, status=status.HTTP_200_OK)
