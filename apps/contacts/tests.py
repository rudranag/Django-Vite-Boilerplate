from django.test import TestCase
from .models import Contact
from django.core.exceptions import ValidationError

class ContactModelTest(TestCase):

    def setUp(self):
        self.contact = Contact.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="1234567890",
            address="123 Main St",
            city="Anytown",
            state="Anystate",
            zip_code="12345",
            country="Anycountry",
            company_name="AnyCompany",
            job_title="Developer",
            birthday="1990-01-01",
            notes="Test note"
        )

    def test_contact_creation(self):
        self.assertIsInstance(self.contact, Contact)
        self.assertEqual(str(self.contact), "John Doe")

    def test_email_uniqueness(self):
        with self.assertRaises(ValidationError):
            duplicate_contact = Contact(
                first_name="Jane",
                last_name="Doe",
                email="john.doe@example.com",  # Duplicate email
                phone_number="0987654321",
                address="456 Another St",
                city="Othertown",
                state="Otherstate",
                zip_code="54321",
                country="Othercountry",
                company_name="OtherCompany",
                job_title="Manager",
                birthday="1985-05-05",
                notes="Another test note"
            )
            duplicate_contact.full_clean()  # This should raise a ValidationError

    def test_max_length_constraints(self):
        contact = Contact(
            first_name="A" * 51,  # Exceeds max_length of 50
            last_name="Doe",
            email="unique.email@example.com",
            phone_number="1234567890",
            address="123 Main St",
            city="Anytown",
            state="Anystate",
            zip_code="12345",
            country="Anycountry",
            company_name="AnyCompany",
            job_title="Developer",
            birthday="1990-01-01",
            notes="Test note"
        )
        with self.assertRaises(ValidationError):
            contact.full_clean()  # This should raise a ValidationError

    def test_optional_fields(self):
        contact = Contact(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            phone_number="1234567890",
            address="123 Main St",
            city="Anytown",
            state="Anystate",
            zip_code="12345",
            country="Anycountry",
            company_name="AnyCompany",
            job_title="Developer"
        )
        contact.full_clean()  # This should not raise any errors
        contact.save()
        self.assertIsInstance(contact, Contact)
        self.assertEqual(str(contact), "Jane Smith")
