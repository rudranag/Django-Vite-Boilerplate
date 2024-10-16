from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.todos.models import Todo

class TodoAPITestCase(APITestCase):

    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

        # Create a todo for user1
        self.todo1 = Todo.objects.create(
            user=self.user1,
            title='User1 Todo',
            description='Todo description for user1',
            completed=False
        )

        # URLs
        self.todo_list_create_url = reverse('todo-list-create')  
        self.todo_detail_url = reverse('todo-detail', args=[self.todo1.id]) 

    def test_todo_list_authenticated(self):
        # Test listing todos for an authenticated user
        self.client.login(username='user1', password='password1')
        response = self.client.get(self.todo_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'User1 Todo')

    def test_todo_list_unauthenticated(self):
        # Test listing todos for an unauthenticated user
        response = self.client.get(self.todo_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_todo_create_authenticated(self):
        # Test creating a todo for an authenticated user
        self.client.login(username='user1', password='password1')
        data = {
            'title': 'New Todo',
            'description': 'New description',
            'completed': False
        }
        response = self.client.post(self.todo_list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 2)
        self.assertEqual(Todo.objects.get(id=response.data['id']).title, 'New Todo')

    def test_todo_create_unauthenticated(self):
        # Test creating a todo for an unauthenticated user
        data = {
            'title': 'New Todo',
            'description': 'New description',
            'completed': False
        }
        response = self.client.post(self.todo_list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_todo_retrieve_authenticated(self):
        # Test retrieving a todo by an authenticated user
        self.client.login(username='user1', password='password1')
        response = self.client.get(self.todo_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'User1 Todo')

    def test_todo_retrieve_unauthenticated(self):
        # Test retrieving a todo by an unauthenticated user
        response = self.client.get(self.todo_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_todo_update_authenticated(self):
        # Test updating a todo by an authenticated user
        self.client.login(username='user1', password='password1')
        data = {
            'title': 'Updated Todo',
            'description': 'Updated description',
            'completed': True
        }
        response = self.client.put(self.todo_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo1.refresh_from_db()
        self.assertEqual(self.todo1.title, 'Updated Todo')
        self.assertEqual(self.todo1.completed, True)

    def test_todo_update_unauthenticated(self):
        # Test updating a todo by an unauthenticated user
        data = {
            'title': 'Updated Todo',
            'description': 'Updated description',
            'completed': True
        }
        response = self.client.put(self.todo_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_todo_delete_authenticated(self):
        # Test deleting a todo by an authenticated user
        self.client.login(username='user1', password='password1')
        response = self.client.delete(self.todo_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)

    def test_todo_delete_unauthenticated(self):
        # Test deleting a todo by an unauthenticated user
        response = self.client.delete(self.todo_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_todo_access_another_user_todo(self):
        # Test that user2 cannot access user1's todo
        self.client.login(username='user2', password='password2')
        response = self.client.get(self.todo_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

