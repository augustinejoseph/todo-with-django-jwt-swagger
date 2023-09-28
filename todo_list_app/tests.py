from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from todo_list_app.models import TodoTask
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.test import APIClient, APITestCase


class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register_user")

    def test_register_valid_user(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_register_existing_user(self):
        User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("login_user")

    def test_login_valid_user(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)

    def test_login_invalid_user(self):
        data = {"username": "nonexistentuser", "password": "invalidpassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TodoTaskViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.tasks_url = reverse("task-list-list")
        self.task = TodoTask.objects.create(name="Test Task", user=self.user)

    def test_create_task(self):
        deadline = timezone.now() + timedelta(days=7)
        data = {
            "name": "New Task",
            "user": self.user.id,
            "deadline": deadline,
        }
        response = self.client.post(self.tasks_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_task_list(self):
        response = self.client.get(self.tasks_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
