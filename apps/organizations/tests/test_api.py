import json
from django.test import TestCase, Client
from apps.organizations.models import Organization
from django.contrib.auth.models import User
import os

PASSWORD = os.environ.get('TEST_PASSWORD', 'password1')


class OrganizationAPITestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password=PASSWORD)
        self.organization1 = Organization.objects.create(name='Org 1')
        self.organization_list_create_url = '/api/v1/organizations/'
        self.organization_detail_url = f'/api/v1/organizations/{self.organization1.id}'
        self.client.login(username='user1', password=PASSWORD)

    def test_organization_list(self):
        response = self.client.get(self.organization_list_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'Org 1')

    def test_organization_create(self):
        data = {'name': 'New Org'}
        response = self.client.post(
            self.organization_list_create_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Organization.objects.count(), 2)
        self.assertEqual(
            Organization.objects.get(id=response.json()['id']).name,
            'New Org'
        )

    def test_organization_retrieve(self):
        response = self.client.get(self.organization_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Org 1')

    def test_organization_update(self):
        data = {'name': 'Updated Org'}
        response = self.client.put(
            self.organization_detail_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.organization1.refresh_from_db()
        self.assertEqual(self.organization1.name, 'Updated Org')

    def test_organization_delete(self):
        response = self.client.delete(self.organization_detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Organization.objects.count(), 0)


class OrganizationAPIAdditionalTests(TestCase):
    """
    Additional tests for the Organization API.
    Testing library/framework: Django's unittest-based test framework
    (django.test.TestCase) with django.test.Client.
    """

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user_additional', password=PASSWORD)
        self.organization1 = Organization.objects.create(name='Org 1')
        self.organization_list_create_url = '/api/v1/organizations/'
        # Note: Existing tests use detail URL without a trailing slash; follow the same convention.
        self.organization_detail_url = f'/api/v1/organizations/{self.organization1.id}'
        self.client.login(username='user_additional', password=PASSWORD)

    # ---------- List endpoint ----------
    def test_organization_list_content_type_json(self):
        response = self.client.get(self.organization_list_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["Content-Type"].startswith("application/json"))

    def test_organization_list_empty(self):
        Organization.objects.all().delete()
        response = self.client.get(self.organization_list_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_organization_list_multiple(self):
        Organization.objects.create(name='Org 2')
        Organization.objects.create(name='Org 3')
        response = self.client.get(self.organization_list_create_url)
        self.assertEqual(response.status_code, 200)
        names = [o.get('name') for o in response.json()]
        self.assertCountEqual(names, ['Org 1', 'Org 2', 'Org 3'])

    # ---------- Retrieve endpoint ----------
    def test_organization_retrieve_not_found(self):
        response = self.client.get('/api/v1/organizations/999999')
        self.assertEqual(response.status_code, 404)

    def test_organization_detail_invalid_id_format(self):
        response = self.client.get('/api/v1/organizations/invalid')
        self.assertEqual(response.status_code, 404)

    # ---------- Create endpoint ----------
    def test_organization_create_missing_name(self):
        data = {}
        response = self.client.post(
            self.organization_list_create_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        body = response.json()
        self.assertIn('name', body)

    def test_organization_create_blank_name(self):
        data = {'name': ''}
        response = self.client.post(
            self.organization_list_create_url,
            json.dumps(data),
            content_type='application/json'
        )
        # DRF standard validation yields 400 for blank required fields.
        self.assertEqual(response.status_code, 400)
        body = response.json()
        self.assertIn('name', body)

    def test_organization_create_invalid_content_type(self):
        response = self.client.post(
            self.organization_list_create_url,
            data='name=Wrong+Type',
            content_type='text/plain'
        )
        # Depending on configuration: 400 (bad request) or 415 (unsupported media type).
        self.assertIn(response.status_code, [400, 415])

    # ---------- Update endpoint ----------
    def test_organization_update_put_missing_name(self):
        response = self.client.put(
            self.organization_detail_url,
            json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        body = response.json()
        self.assertIn('name', body)

    def test_organization_update_invalid_json(self):
        response = self.client.put(
            self.organization_detail_url,
            '}',
            content_type='application/json'
        )
        # DRF ParseError -> 400 Bad Request
        self.assertEqual(response.status_code, 400)

    def test_organization_partial_update_patch(self):
        response = self.client.patch(
            self.organization_detail_url,
            json.dumps({'name': 'Patched Org'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.organization1.refresh_from_db()
        self.assertEqual(self.organization1.name, 'Patched Org')

    # ---------- Delete endpoint ----------
    def test_organization_delete_not_found(self):
        response = self.client.delete('/api/v1/organizations/999999')
        self.assertEqual(response.status_code, 404)

    def test_delete_is_idempotent_second_call_404(self):
        first = self.client.delete(self.organization_detail_url)
        self.assertEqual(first.status_code, 204)
        second = self.client.delete(self.organization_detail_url)
        self.assertEqual(second.status_code, 404)

    # ---------- HTTP method constraints ----------
    def test_methods_not_allowed(self):
        # POST should not be allowed on detail endpoint
        response_detail_post = self.client.post(
            self.organization_detail_url,
            json.dumps({'name': 'Should Fail'}),
            content_type='application/json'
        )
        self.assertEqual(response_detail_post.status_code, 405)

        # PUT should not be allowed on list endpoint
        response_list_put = self.client.put(
            self.organization_list_create_url,
            json.dumps({'name': 'Should Fail'}),
            content_type='application/json'
        )
        self.assertEqual(response_list_put.status_code, 405)

    # ---------- Authentication/authorization ----------
    def test_unauthenticated_access_is_restricted(self):
        self.client.logout()
        response = self.client.get(self.organization_list_create_url)
        # Accept either 401 (Unauthorized) or 403 (Forbidden) depending on settings.
        self.assertIn(response.status_code, [401, 403])