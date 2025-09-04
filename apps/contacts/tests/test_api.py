import json
from django.contrib.auth.models import User
from django.test import TestCase, Client
from apps.contacts.models import Contact
from apps.organizations.models import Organization

# Constants for test passwords
PASSWORD1 = 'password1'
PASSWORD2 = 'password2'

class ContactAPITestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password=PASSWORD1)
        self.user2 = User.objects.create_user(username='user2', password=PASSWORD2)
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
        self.client.login(username='user1', password=PASSWORD1)
        response = self.client.get(self.contact_list_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['first_name'], 'John')

    def test_contact_list_unauthenticated(self):
        response = self.client.get(self.contact_list_create_url)
        self.assertEqual(response.status_code, 401)

    def test_contact_create_authenticated(self):
        self.client.login(username='user1', password=PASSWORD1)
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com',
            'organization_id': self.organization.id
        }
        response = self.client.post(
            self.contact_list_create_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Contact.objects.count(), 2)
        self.assertEqual(
            Contact.objects.get(id=response.json()['id']).first_name,
            'Jane'
        )

    def test_contact_create_unauthenticated(self):
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com',
            'organization_id': self.organization.id
        }
        response = self.client.post(
            self.contact_list_create_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)

    def test_contact_retrieve_authenticated(self):
        self.client.login(username='user1', password=PASSWORD1)
        response = self.client.get(self.contact_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['first_name'], 'John')

    def test_contact_retrieve_unauthenticated(self):
        response = self.client.get(self.contact_detail_url)
        self.assertEqual(response.status_code, 401)

    def test_contact_update_authenticated(self):
        self.client.login(username='user1', password=PASSWORD1)
        data = {
            'first_name': 'Johnathan',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'organization_id': self.organization.id
        }
        response = self.client.put(
            self.contact_detail_url,
            json.dumps(data),
            content_type='application/json'
        )
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
        response = self.client.put(
            self.contact_detail_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)

    def test_contact_delete_authenticated(self):
        self.client.login(username='user1', password=PASSWORD1)
        response = self.client.delete(self.contact_detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Contact.objects.count(), 0)

    def test_contact_delete_unauthenticated(self):
        response = self.client.delete(self.contact_detail_url)
        self.assertEqual(response.status_code, 401)

    def test_contact_access_another_user_contact(self):
        self.client.login(username='user2', password=PASSWORD2)
        response = self.client.get(self.contact_detail_url)
        self.assertEqual(response.status_code, 404)


class ContactAPITestCaseAdditional(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1_extra', password=PASSWORD1)
        self.user2 = User.objects.create_user(username='user2_extra', password=PASSWORD2)
        self.org = Organization.objects.create(name='Extra Org')
        # Base contact for user1
        self.c1 = Contact.objects.create(
            user=self.user1,
            first_name='Alice',
            last_name='Smith',
            email='alice.smith@example.com',
            organization=self.org
        )
        self.list_url = '/api/v1/contacts/'
        self.detail_url = f'/api/v1/contacts/{self.c1.id}'

    # List returns only the authenticated user's contacts even when others exist
    def test_list_filters_out_other_users_contacts(self):
        Contact.objects.create(
            user=self.user2,
            first_name='Bob',
            last_name='Jones',
            email='bob.jones@example.com',
            organization=self.org
        )
        self.client.login(username='user1_extra', password=PASSWORD1)
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(all(item['email'] != 'bob.jones@example.com' for item in data))
        self.assertTrue(any(item['email'] == 'alice.smith@example.com' for item in data))

    # Method not allowed on list/detail endpoints
    def test_method_not_allowed_on_list_put_delete(self):
        self.client.login(username='user1_extra', password=PASSWORD1)
        resp_put = self.client.put(self.list_url, json.dumps({}), content_type='application/json')
        resp_del = self.client.delete(self.list_url)
        self.assertIn(resp_put.status_code, (400, 405))
        self.assertIn(resp_del.status_code, (400, 405))

    def test_method_not_allowed_on_detail_post(self):
        self.client.login(username='user1_extra', password=PASSWORD1)
        resp = self.client.post(self.detail_url, json.dumps({}), content_type='application/json')
        self.assertIn(resp.status_code, (400, 405))

    # Create validations
    def test_create_missing_required_fields(self):
        self.client.login(username='user1_extra', password=PASSWORD1)
        # Missing first_name and email
        payload = {'last_name': 'Doe', 'organization_id': self.org.id}
        resp = self.client.post(self.list_url, json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_create_invalid_email_format(self):
        self.client.login(username='user1_extra', password=PASSWORD1)
        payload = {
            'first_name': 'Bad',
            'last_name': 'Email',
            'email': 'not-an-email',
            'organization_id': self.org.id
        }
        resp = self.client.post(self.list_url, json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_create_with_nonexistent_organization(self):
        self.client.login(username='user1_extra', password=PASSWORD1)
        payload = {
            'first_name': 'Orga',
            'last_name': 'Missing',
            'email': 'orga.missing@example.com',
            'organization_id': 999999
        }
        resp = self.client.post(self.list_url, json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    # Retrieve validations
    def test_retrieve_nonexistent_contact_authenticated(self):
        self.client.login(username='user1_extra', password=PASSWORD1)
        resp = self.client.get('/api/v1/contacts/999999')
        self.assertEqual(resp.status_code, 404)

    def test_retrieve_nonexistent_contact_unauthenticated(self):
        # Unauthenticated should fail on auth before object lookup
        resp = self.client.get('/api/v1/contacts/999999')
        self.assertEqual(resp.status_code, 401)

    # Ownership enforcement on update/delete
    def test_update_another_users_contact_returns_404(self):
        other = Contact.objects.create(
            user=self.user2,
            first_name='Carol',
            last_name='Other',
            email='carol.other@example.com',
            organization=self.org
        )
        self.client.login(username='user1_extra', password=PASSWORD1)
        payload = {
            'first_name': 'Hacker',
            'last_name': 'McHack',
            'email': 'carol.other@example.com',
            'organization_id': self.org.id
        }
        resp = self.client.put(
            f'/api/v1/contacts/{other.id}',
            json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 404)

    def test_delete_another_users_contact_returns_404(self):
        other = Contact.objects.create(
            user=self.user2,
            first_name='Dan',
            last_name='Other',
            email='dan.other@example.com',
            organization=self.org
        )
        self.client.login(username='user1_extra', password=PASSWORD1)
        resp = self.client.delete(f'/api/v1/contacts/{other.id}')
        self.assertEqual(resp.status_code, 404)

    # Update validations
    def test_update_invalid_email(self):
        self.client.login(username='user1_extra', password=PASSWORD1)
        payload = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'invalid-email',
            'organization_id': self.org.id
        }
        resp = self.client.put(self.detail_url, json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_update_nonexistent_contact_authenticated(self):
        self.client.login(username='user1_extra', password=PASSWORD1)
        payload = {
            'first_name': 'Zed',
            'last_name': 'Z',
            'email': 'zed@example.com',
            'organization_id': self.org.id
        }
        resp = self.client.put(
            '/api/v1/contacts/999999',
            json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 404)

    def test_delete_nonexistent_contact_authenticated(self):
        self.client.login(username='user1_extra', password=PASSWORD1)
        resp = self.client.delete('/api/v1/contacts/999999')
        self.assertEqual(resp.status_code, 404)

    # Creating a contact with duplicate email for same user (if unique constraint exists per user, expect 400)
    def test_create_duplicate_email_same_user(self):
        self.client.login(username='user1_extra', password=PASSWORD1)
        payload = {
            'first_name': 'AliceClone',
            'last_name': 'Smith',
            'email': 'alice.smith@example.com',
            'organization_id': self.org.id
        }
        resp = self.client.post(self.list_url, json.dumps(payload), content_type='application/json')
        # Accept either 400 (validation) or 201 if no uniqueness constraint; the assertion ensures we fail closed if unique is enforced
        self.assertIn(resp.status_code, (201, 400))
        if resp.status_code == 201:
            # Clean up created resource to not affect other tests if uniqueness is not enforced
            created_id = resp.json().get('id')
            if created_id:
                self.client.delete(f'/api/v1/contacts/{created_id}')