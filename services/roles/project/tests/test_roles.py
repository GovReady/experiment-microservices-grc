# services/roles/project/tests/test_roles.py


import json
import unittest

from project import db
from project.api.models import Role
from project.tests.base import BaseTestCase


def add_role(name, description):
    role = Role(name=name, description=description)
    db.session.add(role)
    db.session.commit()
    return role


class TestRoleService(BaseTestCase):
    """Tests for the Roles Service."""

    def test_roles(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/roles/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_role(self):
        """Ensure a new role can be added to the database."""
        with self.client:
            response = self.client.post(
                '/roles',
                data=json.dumps({
                    'name': 'ISSO',
                    'description': 'Information System Security Officer'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('ISSO was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_role_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/roles',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_role_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a name key.
        """
        with self.client:
            response = self.client.post(
                '/roles',
                data=json.dumps({'name': 'ISSO'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_role_duplicate_name(self):
        """Ensure error is thrown if the name already exists."""
        with self.client:
            self.client.post(
                '/roles',
                data=json.dumps({
                    'name': 'ISSO',
                    'description': 'Information System Security Officer'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/roles',
                data=json.dumps({
                    'name': 'ISSO',
                    'description': 'Information System Security Officer'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That role already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_role(self):
        """Ensure get single role behaves correctly."""
        role = add_role('ISSO', 'Information System Security Officer')
        with self.client:
            response = self.client.get(f'/roles/{role.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('ISSO', data['data']['name'])
            self.assertIn('Information System Security Officer', data['data']['description'])
            self.assertIn('success', data['status'])

    def test_single_role_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/roles/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Role does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_role_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/role/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Role does not exist', data['message'])
            self.assertIn('fail', data['status'])


    def test_all_roles(self):
        """Ensure get all roles behaves correctly."""
        add_role('ISSO', 'Information System Security Officer')
        add_role('AO', 'Authorizing Official')
        with self.client:
            response = self.client.get('/roles')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['roles']), 2)
            self.assertIn('ISSO', data['data']['roles'][0]['name'])
            self.assertIn(
                'Information System Security Officer', data['data']['roles'][0]['description'])
            self.assertIn('AO', data['data']['roles'][1]['name'])
            self.assertIn(
                'Authorizing Official', data['data']['roles'][1]['description'])
            self.assertIn('success', data['status'])

    def test_main_no_roles(self):
        """Ensure the main route behaves correctly when no roles have been
        added to the database."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Roles', response.data)
        self.assertIn(b'<p>No roles!</p>', response.data)

    def test_main_with_roles(self):
        """Ensure the main route behaves correctly when roles have been
        added to the database."""
        add_role('ISSO', 'Information System Security Officer')
        add_role('AO', 'Authorizing Official')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Roles', response.data)
            self.assertNotIn(b'<p>No roles!</p>', response.data)
            self.assertIn(b'ISSO', response.data)
            self.assertIn(b'AO', response.data)

    def test_main_add_role(self):
        """Ensure a new role can be added to the database."""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(name='ISSO', description='Information System Security Officer'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Roles', response.data)
            self.assertNotIn(b'<p>No roles!</p>', response.data)
            self.assertIn(b'ISSO', response.data)


if __name__ == '__main__':
    unittest.main()
