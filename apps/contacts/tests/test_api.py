import json
from django.contrib.auth.models import User
from django.test import TestCase, Client
from apps.contacts.models import Contact
from apps.organizations.models import Organization

class ContactAPITestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.organization = Organization.objects.create(name='Test Org')
        self.contact1 = Contact.objects.create(
            user=self.user1,
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            organization=self.organization
        )
        self.contact_list_create_url = '/api/v1/contacts/'
        self.contact_detail_url = f'/api/v1/contacts/{self.contact1.id}'

    def test_contact_list_authenticated(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(self.contact_list_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['first_name'], 'John')

    def test_contact_list_unauthenticated(self):
        response = self.client.get(self.contact_list_create_url)
        self.assertEqual(response.status_code, 401)

    def test_contact_create_authenticated(self):
        self.client.login(username='user1', password='password1')
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com',
            'organization_id': self.organization.id
        }
        response = self.client.post(self.contact_list_create_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Contact.objects.count(), 2)
        self.assertEqual(Contact.objects.get(id=response.json()['id']).first_name, 'Jane')

    def test_contact_create_unauthenticated(self):
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com',
            'organization_id': self.organization.id
        }
        response = self.client.post(self.contact_list_create_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_contact_retrieve_authenticated(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(self.contact_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['first_name'], 'John')

    def test_contact_retrieve_unauthenticated(self):
        response = self.client.get(self.contact_detail_url)
        self.assertEqual(response.status_code, 401)

    def test_contact_update_authenticated(self):
        self.client.login(username='user1', password='password1')
        data = {
            'first_name': 'Johnathan',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'organization_id': self.organization.id
        }
        response = self.client.put(self.contact_detail_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.contact1.refresh_from_db()
        self.assertEqual(self.contact1.first_name, 'Johnathan')

    def test_contact_update_unauthenticated(self):
        data = {
            'first_name': 'Johnathan',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'organization_id': self.organization.id
        }
        response = self.client.put(self.contact_detail_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_contact_delete_authenticated(self):
        self.client.login(username='user1', password='password1')
        response = self.client.delete(self.contact_detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Contact.objects.count(), 0)

    def test_contact_delete_unauthenticated(self):
        response = self.client.delete(self.contact_detail_url)
        self.assertEqual(response.status_code, 401)

    def test_contact_access_another_user_contact(self):
        self.client.login(username='user2', password='password2')
        response = self.client.get(self.contact_detail_url)
        self.assertEqual(response.status_code, 404)
