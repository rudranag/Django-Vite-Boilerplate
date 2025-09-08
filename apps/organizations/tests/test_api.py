import json
from django.test import TestCase, Client
from apps.organizations.models import Organization
from django.contrib.auth.models import User


class OrganizationAPITestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.organization1 = Organization.objects.create(name='Org 1')
        self.organization_list_create_url = '/api/v1/organizations/'
        self.organization_detail_url = f'/api/v1/organizations/{self.organization1.id}'
        self.client.login(username='user1', password='password1')

    def test_organization_list(self):
        response = self.client.get(self.organization_list_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'Org 1')

    def test_organization_create(self):
        data = {'name': 'New Org'}
        response = self.client.post(self.organization_list_create_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Organization.objects.count(), 2)
        self.assertEqual(Organization.objects.get(id=response.json()['id']).name, 'New Org')

    def test_organization_retrieve(self):
        response = self.client.get(self.organization_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Org 1')

    def test_organization_update(self):
        data = {'name': 'Updated Org'}
        response = self.client.put(self.organization_detail_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.organization1.refresh_from_db()
        self.assertEqual(self.organization1.name, 'Updated Org')

    def test_organization_delete(self):
        response = self.client.delete(self.organization_detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Organization.objects.count(), 0)
