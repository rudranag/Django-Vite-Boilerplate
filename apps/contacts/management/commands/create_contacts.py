from django.core.management.base import BaseCommand
from faker import Faker
from apps.contacts.models import Contact  # Replace 'myapp' with the name of your app

class Command(BaseCommand):
    help = 'Generate fake contacts'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Indicates the number of contacts to be created')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        fake = Faker()

        contacts = []
        for _ in range(count):
            contact = Contact(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                phone_number=fake.phone_number(),
                address=fake.address(),
                city=fake.city(),
                state=fake.state(),
                zip_code=fake.zipcode(),
                country=fake.country(),
                company_name=fake.company(),
                job_title=fake.job(),
                birthday=fake.date_of_birth(minimum_age=18, maximum_age=70),
                notes=fake.text(max_nb_chars=200),
            )
            contacts.append(contact)

        Contact.objects.bulk_create(contacts)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} contacts'))
