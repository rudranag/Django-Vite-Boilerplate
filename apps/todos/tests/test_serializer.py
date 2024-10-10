from django.test import TestCase
from django.contrib.auth.models import User
from apps.todos.models import Todo
from apps.todos.serializers import TodoSerializer
from django.utils.dateparse import parse_datetime


class TodoSerializerTest(TestCase):

    def setUp(self):
        # Create a user instance for testing
        self.user = User.objects.create_user(username="testuser", password="password")
        self.todo = Todo.objects.create(
            user=self.user,
            title="Test Todo",
            description="This is a test todo item",
            completed=False,
        )
        self.serializer = TodoSerializer(instance=self.todo)

    def test_serializer_fields(self):
        # Test that the serializer includes the correct fields
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set(["id", "title", "description", "completed", "created_at"]),
        )

    def test_serializer_data(self):
        # Test that the serializer data matches the Todo instance
        data = self.serializer.data
        self.assertEqual(data["id"], self.todo.id)
        self.assertEqual(data["title"], self.todo.title)
        self.assertEqual(data["description"], self.todo.description)
        self.assertEqual(data["completed"], self.todo.completed)

        # Parse both dates to ensure they are in the same format before comparison
        created_at_serializer = parse_datetime(data["created_at"])
        created_at_model = self.todo.created_at

        # Compare the datetime objects directly
        self.assertEqual(created_at_serializer, created_at_model)

    def test_serializer_validation_valid_data(self):
        # Test that valid data deserializes correctly
        data = {
            "title": "New Todo",
            "description": "New Description",
            "completed": True,
        }
        serializer = TodoSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        todo = serializer.save(user=self.user)
        self.assertEqual(todo.title, data["title"])
        self.assertEqual(todo.description, data["description"])
        self.assertTrue(todo.completed)

    def test_serializer_validation_invalid_data(self):
        # Test that invalid data raises validation errors
        data = {
            "title": "",  # Title is required, so an empty string should raise an error
            "description": "New Description",
            "completed": True,
        }
        serializer = TodoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
