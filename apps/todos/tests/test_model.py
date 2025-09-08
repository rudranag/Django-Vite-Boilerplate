from django.test import TestCase
from django.contrib.auth.models import User
from apps.todos.models import Todo


class TodoModelTest(TestCase):

    def setUp(self):
        # Create a user instance for testing
        self.user = User.objects.create_user(username="testuser", password="password")
        self.todo = Todo.objects.create(
            user=self.user,
            title="Test Todo",
            description="This is a test todo item",
            completed=False,
        )

    def test_todo_creation(self):
        # Test if the Todo instance is created successfully
        self.assertIsInstance(self.todo, Todo)
        self.assertEqual(self.todo.title, "Test Todo")
        self.assertEqual(self.todo.description, "This is a test todo item")
        self.assertFalse(self.todo.completed)
        self.assertEqual(self.todo.user, self.user)

    def test_todo_str_method(self):
        # Test the string representation of the Todo instance
        self.assertEqual(str(self.todo), "Test Todo")

    def test_todo_default_completed(self):
        # Test that the default value for completed is False
        new_todo = Todo.objects.create(
            user=self.user,
            title="Another Test Todo",
            description="Another test todo item",
        )
        self.assertFalse(new_todo.completed)

    def test_todo_created_at_auto_now_add(self):
        # Test if created_at is set automatically
        self.assertIsNotNone(self.todo.created_at)

    def test_todo_can_be_marked_completed(self):
        # Test marking a todo as completed
        self.todo.completed = True
        self.todo.save()
        self.assertTrue(self.todo.completed)

    def test_todo_update(self):
        # Test updating the Todo instance
        self.todo.title = "Updated Title"
        self.todo.description = "Updated Description"
        self.todo.save()
        updated_todo = Todo.objects.get(id=self.todo.id)
        self.assertEqual(updated_todo.title, "Updated Title")
        self.assertEqual(updated_todo.description, "Updated Description")

    def test_todo_delete(self):
        # Test deleting the Todo instance
        self.todo.delete()
        with self.assertRaises(Todo.DoesNotExist):
            Todo.objects.get(id=self.todo.id)

    def test_user_deletion_cascades(self):
        # Test that deleting the user deletes the associated Todo
        self.user.delete()
        with self.assertRaises(Todo.DoesNotExist):
            Todo.objects.get(id=self.todo.id)

    def test_todo_completed_toggle(self):
        # Test toggling the completed field
        self.todo.completed = not self.todo.completed
        self.todo.save()
        self.assertTrue(self.todo.completed)

        self.todo.completed = not self.todo.completed
        self.todo.save()
        self.assertFalse(self.todo.completed)

    def test_todo_created_at_immutable(self):
        # Test that created_at does not change on update
        original_created_at = self.todo.created_at
        self.todo.title = "Updated Title Again"
        self.todo.save()
        updated_todo = Todo.objects.get(id=self.todo.id)
        self.assertEqual(updated_todo.created_at, original_created_at)
