from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import FriendRequest, User
from rest_framework_simplejwt.tokens import AccessToken
import time
from django.conf import settings

class FriendRequestDetailAPITestCase(APITestCase):
    """
    Test cases for friend requests CRUD operations.
    """

    def setUp(self):
        """
        Set up the test data.
        """
        self.sender = User.objects.create_user(email='sender@example.com', name="sender", password='Password@123')
        self.receiver = User.objects.create_user(email='receiver@example.com', name="receiver", password='Password@123')
        self.token = str(AccessToken.for_user(self.sender))

    def test_send_friend_request(self):
        """
        Test sending a friend request.
        """
        url = reverse('friend_requests')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, data={'receiver_id': self.receiver.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(FriendRequest.objects.filter(sender=self.sender, receiver=self.receiver).exists())

    def test_send_friend_request_to_self(self):
        """
        Test sending a friend request to self.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        url = reverse('friend_requests')
        response = self.client.post(url, data={'receiver_id': self.sender.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(FriendRequest.objects.filter(sender=self.sender, receiver=self.sender).exists())

    def test_accept_friend_request(self):
        """
        Test accepting a friend request.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        friend_request = FriendRequest.objects.create(sender=self.sender, receiver=self.receiver)
        url = reverse('friend_request_detail', kwargs={'request_id': friend_request.id})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        friend_request.refresh_from_db()
        self.assertEqual(friend_request.status, 'accepted')

    def test_reject_friend_request(self):
        """
        Test rejecting a friend request.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        friend_request = FriendRequest.objects.create(sender=self.sender, receiver=self.receiver)
        url = reverse('friend_request_detail', kwargs={'request_id': friend_request.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_pending_friend_request(self):
        """
        Test listing pending friend requests.
        """
        friend1 = User.objects.create_user(email="friend1@example.com", name='friend1', password='Password@123')
        friend2 = User.objects.create_user(email="friend2@example.com", name='friend2', password='Password@123')
        FriendRequest.objects.create(sender=friend1, receiver=self.sender, status='pending')
        FriendRequest.objects.create(sender=friend2, receiver=self.sender, status='pending')

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(reverse('friend_requests'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_accepting_other_user_friend_request(self):
        """
        Test accepting a friend request from another user credentials.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        friend1 = User.objects.create_user(email="friend1@example.com", name='friend1', password='Password@123')
        friend_request = FriendRequest.objects.create(sender=friend1, receiver=self.receiver)
        url = reverse('friend_request_detail', kwargs={'request_id': friend_request.id})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_rejecting_other_user_friend_request(self):
        """
        Test rejecting a friend request from another user credentials.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        friend1 = User.objects.create_user(email="friend1@example.com", name='friend1', password='Password@123')
        friend_request = FriendRequest.objects.create(sender=friend1, receiver=self.receiver)
        url = reverse('friend_request_detail', kwargs={'request_id': friend_request.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_max_friend_requests_per_minute(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        # Send multiple friend requests within a minute
        for i in range(settings.MAX_FRIEND_REQUESTS_PER_MINUTE + 1):
            url = reverse('friend_requests')
            receiver = User.objects.create_user(email=f'receiver{i}@example.com', name=f"receiver{i}", password='Password@123')
            response = self.client.post(url, data={'receiver_id': receiver.id})
            time.sleep(0.1)  
        # Check if the last request returns a rate limit exceeded error
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        # Check if only `MAX_FRIEND_REQUESTS_PER_MINUTE` friend requests are created
        self.assertEqual(FriendRequest.objects.filter(sender=self.sender).count(), settings.MAX_FRIEND_REQUESTS_PER_MINUTE)

    def test_auth_send_friend_request(self):
        """
        Test sending a friend request without authentication.
        """
        url = reverse('friend_requests')
        response = self.client.post(url, data={'receiver_id': self.receiver.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_accepting_friend_request(self):
        """
        Test accepting a friend request without authentication.
        """
        friend_request = FriendRequest.objects.create(sender=self.sender, receiver=self.receiver)
        url = reverse('friend_request_detail', kwargs={'request_id': friend_request.id})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_rejecting_friend_request(self):
        """
        Test accepting a friend request without authentication.
        """
        friend_request = FriendRequest.objects.create(sender=self.sender, receiver=self.receiver)
        url = reverse('friend_request_detail', kwargs={'request_id': friend_request.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_list_friend_request(self):
        """
        Test listing friend requests without authentication.
        """
        url = reverse('friend_requests')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
