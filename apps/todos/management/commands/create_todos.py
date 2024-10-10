from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from apps.todos.models import Todo  # Replace 'todos' with the correct app name


class Command(BaseCommand):
    help = "Generate fake todos for the first user"

    def add_arguments(self, parser):
        parser.add_argument(
            "count", type=int, help="Indicates the number of todos to be created"
        )

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        fake = Faker()

        # Get the first user in the auth_user table
        try:
            user = User.objects.first()
            if not user:
                self.stdout.write(
                    self.style.ERROR("No user found in the auth_user table")
                )
                return
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("No user found in the auth_user table"))
            return

        todos = []
        for _ in range(count):
            todo = Todo(
                user=user,
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                completed=fake.boolean(),
                created_at=fake.date_time_this_year(),
            )
            todos.append(todo)

        Todo.objects.bulk_create(todos)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {count} todos for user {user.username}"
            )
        )
