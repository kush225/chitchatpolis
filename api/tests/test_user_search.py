from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import User
from rest_framework_simplejwt.tokens import AccessToken

class UserSearchTestCase(APITestCase):
    def setUp(self):
        # Create some sample users for testing
        for i in range(1, 16):
            User.objects.create(email=f'user{i}@example.com', name=f'User {i}')

        # Create a user for authentication
        self.user = User.objects.create_user(email='test@example.com', name='Test', password='Password@123')

        # Generate access token for the user
        self.token = str(AccessToken.for_user(self.user))


    def test_auth(self):
        # Test searching for a user by email
        url = reverse('user_search', kwargs={'search_keyword': 'user1@example.com'})

        response = self.client.get(url)

        # Assert status code is returned as 401 in the response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_search_by_email(self):
        # Test searching for a user by email
        url = reverse('user_search', kwargs={'search_keyword': 'user1@example.com'})

        # Authenticate the client with the token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert only one user is returned in the response
        self.assertEqual(response.data['count'], 1)
        # Assert the returned user's email matches the search keyword
        self.assertEqual(response.data['results'][0]['email'], 'user1@example.com')

    def test_search_by_name(self):
        # Test searching for users by name
        url = reverse('user_search', kwargs={'search_keyword': 'User'})

        # Authenticate the client with the token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert all users with names containing 'User' are returned in the response
        self.assertEqual(response.data['count'], 15)

    def test_pagination(self):
        # Test pagination
        url = reverse('user_search', kwargs={'search_keyword': 'User'})

        # Authenticate the client with the token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        response = self.client.get(url + '?page=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that 10 results are returned in the first page
        self.assertEqual(len(response.data['results']), 10)  
        
        # Get the URL for the next page
        next_page_url = response.data['next'] 
        # Make a request to the next page
        response = self.client.get(next_page_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that 5 results are returned in the second page
        self.assertEqual(len(response.data['results']), 5)
