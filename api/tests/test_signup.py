from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import User

class SignUpTestCase(APITestCase):
    def test_signup(self):
        # Define the URL for the signup endpoint
        url = reverse('signup')
        
        # Prepare sample data for signup
        data = {
            'email': 'test@example.com',
            'name': 'Test',
            'password': 'Password@123'
        }
        
        # Make a POST request to the signup endpoint with sample data
        response = self.client.post(url, data, format='json')
        
        # Assert that the response status code is 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check if user is created in the database
        self.assertTrue(User.objects.filter(email=data['email']).exists())
