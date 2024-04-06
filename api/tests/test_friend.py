from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import FriendRequest, Friend, User
from rest_framework_simplejwt.tokens import AccessToken


class ListFriendsAPITestCase(APITestCase):
    """
    Test case to list friends.
    """

    def setUp(self):
        """
        Set up the test data.
        """
        self.user = User.objects.create_user(email="test@example.com", name='test_user', password='Password@123')
        self.friend1 = User.objects.create_user(email="friend1@example.com", name='friend1', password='Password@123')
        self.friend2 = User.objects.create_user(email="friend2@example.com", name='friend2', password='Password@123')
        FriendRequest.objects.create(sender=self.user, receiver=self.friend1, status='accepted')
        FriendRequest.objects.create(sender=self.friend2, receiver=self.user, status='accepted')
        Friend.objects.create(user1=self.user, user2=self.friend1)
        Friend.objects.create(user1=self.user, user2=self.friend2)

        self.token = str(AccessToken.for_user(self.user))

    def test_list_friends(self):
        """
        Test listing friends for authenticated user.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(reverse('friend'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_auth_list_friend(self):
        """
        Test listing friends for unauthenticated user.
        """
        response = self.client.get(reverse('friend'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
