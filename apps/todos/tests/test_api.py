import json
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from apps.todos.models import Todo


class TodoAPITestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.password1 = 'password1'
        self.password2 = 'password2'
        # Create two users
        self.user1 = User.objects.create_user(username='user1', password=self.password1)
        self.user2 = User.objects.create_user(username='user2', password=self.password2)

        # Create a todo for user1
        self.todo1 = Todo.objects.create(
            user=self.user1,
            title='User1 Todo',
            description='Todo description for user1',
            completed=False
        )

        # URLs
        self.todo_list_create_url = '/api/v1/todos/'
        self.todo_detail_url = f'/api/v1/todos/{self.todo1.id}'

    def test_todo_list_authenticated(self):
        # Test listing todos for an authenticated user
        self.client.login(username='user1', password=self.password1)
        response = self.client.get(self.todo_list_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['title'], 'User1 Todo')

    def test_todo_list_unauthenticated(self):
        # Test listing todos for an unauthenticated user
        response = self.client.get(self.todo_list_create_url)
        self.assertEqual(response.status_code, 401)

    def test_todo_create_authenticated(self):
        # Test creating a todo for an authenticated user
        self.client.login(username='user1', password=self.password1)
        data = {
            'title': 'New Todo',
            'description': 'New description',
            'completed': False
        }
        response = self.client.post(self.todo_list_create_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Todo.objects.count(), 2)
        self.assertEqual(Todo.objects.get(id=response.json()['id']).title, 'New Todo')

    def test_todo_create_unauthenticated(self):
        # Test creating a todo for an unauthenticated user
        data = {
            'title': 'New Todo',
            'description': 'New description',
            'completed': False
        }
        response = self.client.post(self.todo_list_create_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_todo_retrieve_authenticated(self):
        # Test retrieving a todo by an authenticated user
        self.client.login(username='user1', password=self.password1)
        response = self.client.get(self.todo_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'User1 Todo')

    def test_todo_retrieve_unauthenticated(self):
        # Test retrieving a todo by an unauthenticated user
        response = self.client.get(self.todo_detail_url)
        self.assertEqual(response.status_code, 401)

    def test_todo_update_authenticated(self):
        # Test updating a todo by an authenticated user
        self.client.login(username='user1', password=self.password1)
        data = {
            'title': 'Updated Todo',
            'description': 'Updated description',
            'completed': True
        }
        response = self.client.put(self.todo_detail_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.todo1.refresh_from_db()
        self.assertEqual(self.todo1.title, 'Updated Todo')
        self.assertTrue(self.todo1.completed)

    def test_todo_update_unauthenticated(self):
        # Test updating a todo by an unauthenticated user
        data = {
            'title': 'Updated Todo',
            'description': 'Updated description',
            'completed': True
        }
        response = self.client.put(self.todo_detail_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_todo_delete_authenticated(self):
        # Test deleting a todo by an authenticated user
        self.client.login(username='user1', password=self.password1)
        response = self.client.delete(self.todo_detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Todo.objects.count(), 0)

    def test_todo_delete_unauthenticated(self):
        # Test deleting a todo by an unauthenticated user
        response = self.client.delete(self.todo_detail_url)
        self.assertEqual(response.status_code, 401)

    def test_todo_access_another_user_todo(self):
        # Test that user2 cannot access user1's todo
        self.client.login(username='user2', password=self.password2)
        response = self.client.get(self.todo_detail_url)
        self.assertEqual(response.status_code, 404)

    def test_todo_list_shows_only_authenticated_users_items(self):
        # user1 already has self.todo1
        # Create a todo for user2 that should not appear for user1
        Todo.objects.create(
            user=self.user2,
            title='User2 Todo',
            description='Todo description for user2',
            completed=False
        )
        self.client.login(username='user1', password=self.password1)
        response = self.client.get(self.todo_list_create_url)
        self.assertEqual(response.status_code, 200)
        # Ensure only user1's todos are returned
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'User1 Todo')

    def test_todo_retrieve_nonexistent_returns_404(self):
        self.client.login(username='user1', password=self.password1)
        response = self.client.get('/api/v1/todos/999999')
        self.assertEqual(response.status_code, 404)

    def test_todo_create_invalid_json_returns_400(self):
        self.client.login(username='user1', password=self.password1)
        # Send invalid JSON payload
        response = self.client.post(self.todo_list_create_url, "{invalid json", content_type='application/json')
        self.assertIn(response.status_code, [400, 422])  # Accept either 400 Bad Request or 422 Unprocessable Entity

    def test_todo_create_missing_title_returns_400(self):
        self.client.login(username='user1', password=self.password1)
        data = {
            # 'title' missing
            'description': 'Missing title',
            'completed': False
        }
        response = self.client.post(self.todo_list_create_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_todo_create_invalid_completed_type_returns_400(self):
        self.client.login(username='user1', password=self.password1)
        data = {
            'title': 'Invalid completed',
            'description': 'completed should be boolean',
            'completed': 'yes'  # invalid type
        }
        response = self.client.post(self.todo_list_create_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_todo_create_defaults_completed_to_false_when_omitted(self):
        self.client.login(username='user1', password=self.password1)
        data = {
            'title': 'Default completed',
            'description': 'completed omitted'
        }
        response = self.client.post(self.todo_list_create_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        created = Todo.objects.get(id=response.json()['id'])
        self.assertFalse(created.completed)

    def test_todo_update_invalid_completed_type_returns_400(self):
        self.client.login(username='user1', password=self.password1)
        data = {
            'title': 'Keep Title',
            'description': 'Bad type for completed',
            'completed': 'not-a-bool'
        }
        response = self.client.put(self.todo_detail_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_todo_update_nonexistent_returns_404(self):
        self.client.login(username='user1', password=self.password1)
        data = {
            'title': 'Does not matter',
            'description': 'Not found case',
            'completed': False
        }
        response = self.client.put('/api/v1/todos/999999', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_todo_delete_nonexistent_returns_404(self):
        self.client.login(username='user1', password=self.password1)
        response = self.client.delete('/api/v1/todos/999999')
        self.assertEqual(response.status_code, 404)

    def test_todo_update_another_users_todo_returns_404(self):
        # user2 attempts to update user1's todo
        self.client.login(username='user2', password=self.password2)
        data = {
            'title': 'Hacked Update',
            'description': 'Should not be allowed',
            'completed': True
        }
        response = self.client.put(self.todo_detail_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        # Ensure original todo unchanged
        self.todo1.refresh_from_db()
        self.assertEqual(self.todo1.title, 'User1 Todo')
        self.assertFalse(self.todo1.completed)

    def test_todo_delete_another_users_todo_returns_404(self):
        # user2 attempts to delete user1's todo
        self.client.login(username='user2', password=self.password2)
        response = self.client.delete(self.todo_detail_url)
        self.assertEqual(response.status_code, 404)
        # Ensure still exists
        self.assertEqual(Todo.objects.filter(id=self.todo1.id).count(), 1)

    def test_todo_method_not_allowed_on_list_detail(self):
        self.client.login(username='user1', password=self.password1)
        # POST on detail should be method not allowed
        response = self.client.post(self.todo_detail_url, json.dumps({'title': 'X'}), content_type='application/json')
        self.assertIn(response.status_code, [405, 404])  # Some routers may return 404 for unsupported
        # PUT on list should be method not allowed
        response = self.client.put(self.todo_list_create_url, json.dumps({'title': 'X'}), content_type='application/json')
        self.assertIn(response.status_code, [405, 400])  # Depending on router, 405 or validation 400

    def test_todo_list_unauthenticated_does_not_leak_data(self):
        # Create another todo to ensure there is data present
        Todo.objects.create(
            user=self.user2,
            title='User2 Another Todo',
            description='Should not leak',
            completed=False
        )
        response = self.client.get(self.todo_list_create_url)
        self.assertEqual(response.status_code, 401)