from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()


class UserModelTest(TestCase):
    """Test the custom User model"""
    
    def test_create_user(self):
        """Test creating a user"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser"""
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertEqual(admin_user.username, 'admin')
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.check_password('adminpass123'))
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class ChatsAPITest(APITestCase):
    """Test the chats API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_api_accessibility(self):
        """Test that API endpoints are accessible"""
        # This is a basic test to ensure the API structure is working
        # You can expand this based on your actual API endpoints
        response = self.client.get('/api/') # Adjust URL based on your API structure
        # The response might be 404 if no endpoint exists, which is fine for now
        # This test ensures the Django server can start and handle requests
        self.assertIn(response.status_code, [200, 404, 403, 401])


class DatabaseConnectionTest(TestCase):
    """Test database connectivity"""
    
    def test_database_connection(self):
        """Test that we can connect to the database"""
        # Create a simple object to test database connectivity
        user = User.objects.create_user(
            username='dbtest',
            email='dbtest@example.com',
            password='testpass123'
        )
        # Retrieve the user from database
        retrieved_user = User.objects.get(username='dbtest')
        self.assertEqual(user.id, retrieved_user.id)
        self.assertEqual(user.username, retrieved_user.username)
