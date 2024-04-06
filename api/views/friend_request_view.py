from rest_framework import generics, status
from rest_framework.response import Response
from ..models import FriendRequest
from ..serializers.friend_request_serializer import FriendRequestSerializer, FriendRequestUpdateSerializer
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
import logging

logger = logging.getLogger(__name__)

class FriendRequestListAPIView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating friend requests.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer

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
            
            if FriendRequest.objects.filter(sender=sender, receiver_id=receiver.id, status='pending').exists():
                return Response({"error": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)
            
            recent_requests = FriendRequest.objects.filter(sender=sender, created_at__gte=timezone.now() - timedelta(minutes=1)).count()
            if recent_requests >= settings.MAX_FRIEND_REQUESTS_PER_MINUTE:
                return Response({"error": "Rate limit exceeded"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            
            friend_request = serializer.save(sender=sender)
            logger.info(f"Friend request sent from {sender.email} to {receiver.email}")
            return Response(self.serializer_class(friend_request).data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Invalid friend request data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FriendRequestDetailAPIView(generics.UpdateAPIView):
    """
    API endpoint for updating friend requests.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestUpdateSerializer
    queryset = FriendRequest.objects.all()
    lookup_url_kwarg = 'request_id'

    def update(self, request, *args, **kwargs):
        """
        Update the status of a friend request.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            fr_status = serializer.validated_data.get('status') 
            serializer = self.get_serializer(instance, data={'status': fr_status}, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            logger.info(f"Friend request status updated: {fr_status}")
            return Response({"message": f"Friend request {fr_status}"}, status=status.HTTP_200_OK)
        else:
            logger.error(f"Invalid friend request status: {serializer.errors}")
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
