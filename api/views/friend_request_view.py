from rest_framework import generics, status
from rest_framework.response import Response
from ..models import FriendRequest, Friend
from ..serializers.friend_request_serializer import FriendRequestSerializer, FriendRequestUpdateSerializer
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
import logging
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Q
from rest_framework.throttling import UserRateThrottle

logger = logging.getLogger(__name__)

class FriendRequestListAPIView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating friend requests.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        """
        Get the queryset of pending friend requests for the current user.
        """
        return FriendRequest.objects.filter(receiver=self.request.user, status='pending')

    def post(self, request, *args, **kwargs):
        """
        Create a new friend request.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            sender = request.user
            receiver = serializer.validated_data.get('receiver')
            if sender.id == receiver.id:
                return Response({"error": "Cannot send friend request to self"}, status=status.HTTP_400_BAD_REQUEST)
            
            record = FriendRequest.objects.filter(sender=sender, receiver_id=receiver.id, status__in=('pending', 'accepted')).last()
            if record:
                if record.status == 'pending':
                    return Response({"error": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)
                elif record.status == 'accepted':
                    return Response({"error": "Already a friend"}, status=status.HTTP_400_BAD_REQUEST)

            friend_request = serializer.save(sender=sender)
            logger.info(f"Friend request sent from {sender.email} to {receiver.email}")
            return Response(self.serializer_class(friend_request).data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Invalid friend request data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FriendRequestDetailAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    """
    API endpoint for updating friend requests.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestUpdateSerializer
    queryset = FriendRequest.objects.all()

    def get_object(self):
        pk = self.kwargs.get('request_id')
        user = self.request.user
        queryset = self.queryset.filter(Q(pk=pk, receiver=user, status="pending") | Q(pk=pk, sender=user, status="pending"))
        return get_object_or_404(queryset)

    def partial_update(self, request, *args, **kwargs):
        """
        Update the status of a friend request and add friend.
        """
        instance = self.get_object()

        serializer = self.get_serializer(instance, data={'status': "accepted"})
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            serializer.save()

            # Create a friend relationship
            Friend.objects.create(user1=instance.sender, user2=instance.receiver)
            logger.info(f"Friend created")
            return Response(status=status.HTTP_204_NO_CONTENT)
        

    def delete(self, request, *args, **kwargs):
        """
        Delete the friend request.
        """
        instance = self.get_object()
        instance.delete()
        logger.info(f"Friend request deleted")
        return Response(status=status.HTTP_204_NO_CONTENT)
