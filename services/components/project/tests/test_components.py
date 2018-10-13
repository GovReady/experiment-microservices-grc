# services/commponents/project/tests/test_components.py


import json
import unittest

from project import db
from project.api.models import Component
from project.tests.base import BaseTestCase


def add_component(name, description):
    component = Component(name=name, description=description)
    db.session.add(component)
    db.session.commit()
    return component


class TestComponentService(BaseTestCase):
    """Tests for the Components Service."""

    def test_components(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/components/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_component(self):
        """Ensure a new component can be added to the database."""
        with self.client:
            response = self.client.post(
                '/components',
                data=json.dumps({
                    'name': 'aws',
                    'description': 'Amazon Web Services'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('aws was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_component_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/components',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_component_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a name key.
        """
        with self.client:
            response = self.client.post(
                '/components',
                data=json.dumps({'name': 'aws'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_component_duplicate_name(self):
        """Ensure error is thrown if the name already exists."""
        with self.client:
            self.client.post(
                '/components',
                data=json.dumps({
                    'name': 'aws',
                    'description': 'Amazon Web Services'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/components',
                data=json.dumps({
                    'name': 'aws',
                    'description': 'Amazon Web Services'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That component already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_component(self):
        """Ensure get single component behaves correctly."""
        component = add_component('aws', 'Amazon Web Services')
        with self.client:
            response = self.client.get(f'/components/{component.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('aws', data['data']['name'])
            self.assertIn('Amazon Web Services', data['data']['description'])
            self.assertIn('success', data['status'])

    def test_single_component_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/components/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Component does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_component_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/component/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Component does not exist', data['message'])
            self.assertIn('fail', data['status'])


    def test_all_components(self):
        """Ensure get all components behaves correctly."""
        add_component('aws', 'Amazon Web Services')
        add_component('Azure', 'Microsoft Azure')
        with self.client:
            response = self.client.get('/components')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['components']), 2)
            self.assertIn('aws', data['data']['components'][0]['name'])
            self.assertIn(
                'Amazon Web Services', data['data']['components'][0]['description'])
            self.assertIn('Azure', data['data']['components'][1]['name'])
            self.assertIn(
                'Authorizing Official', data['data']['components'][1]['description'])
            self.assertIn('success', data['status'])

    def test_main_no_components(self):
        """Ensure the main route behaves correctly when no components have been
        added to the database."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Components', response.data)
        self.assertIn(b'<p>No components!</p>', response.data)

    def test_main_with_components(self):
        """Ensure the main route behaves correctly when components have been
        added to the database."""
        add_component('aws', 'Amazon Web Services')
        add_component('Azure', 'Authorizing Official')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Components', response.data)
            self.assertNotIn(b'<p>No components!</p>', response.data)
            self.assertIn(b'aws', response.data)
            self.assertIn(b'Azure', response.data)

    def test_main_add_component(self):
        """Ensure a new component can be added to the database."""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(name='aws', description='Amazon Web Services'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Components', response.data)
            self.assertNotIn(b'<p>No components!</p>', response.data)
            self.assertIn(b'aws', response.data)


if __name__ == '__main__':
    unittest.main()
