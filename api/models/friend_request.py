from django.db import models
from typing import Tuple
from .user import User


STATUS_CHOICES: Tuple[str, str] = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
)

class FriendRequest(models.Model):
    """
    Model representing a friend request sent from one user to another.
    """

    
    sender: models.ForeignKey[User, models.CASCADE] = models.ForeignKey(User, related_name='sent_friend_requests', on_delete=models.CASCADE)
    receiver: models.ForeignKey[User, models.CASCADE] = models.ForeignKey(User, related_name='received_friend_requests', on_delete=models.CASCADE)
    status: models.CharField = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta class containing additional information about the model.
        """
        unique_together = ['sender', 'receiver']
