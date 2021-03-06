import os
from flask import Flask
from functools import wraps
from unittest.mock import patch
import unittest
import json
from api import app
from api.controllers.errors import errorhandler_app
from api.database import create_db


def mock_func(x=''):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            payload = x
            return f(payload, *args, **kwargs)
        return wrapper
    return decorator

""" overiding requires_auth decorator """
patch('api.controllers.farmers.requires_auth', mock_func).start()
from api.controllers.farmers import farmers_app
from api.models.farmer import Farmer
from api.database import db

myApp = Flask(__name__)
myApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database_path = os.environ['TEST_DATABASE_URL']

create_db(myApp, database_path)
farmers_app(myApp)
errorhandler_app(myApp)

class FarmersTestCase(unittest.TestCase):

    def setUp(self):
        self.client = myApp.test_client()
        db.create_all()

        db.session.add(
            Farmer(
            firstname='john',
            lastname='dee',
            phone='123',
            email='john@oaf.oaf',
            country= 'ug',
            state='kla',
            village='kaz'
            )
        )

        db.session.commit()
        self.farmer = Farmer.query.first()
        db.session.close()

    def tearDown(self):
        db.drop_all()

    def test_get_farmers(self):
        """ Test get farmers endpoint """
        response = self.client.get('/farmers')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']), 1)

    def test_get_farmers_with_wrong_method(self):
        """ Test get farmers endpoint """
        response = self.client.put('/farmers')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 405)
        self.assertFalse(data['success'])

    def test_get_farmers_with_wrong_endpoint(self):
        """ Test get farmers endpoint """
        response = self.client.get('/farmerss')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        
    def test_post_farmers(self):
        """ Test get farmers endpoint """
        body = {
            'firstname': 'peter',
            'lastname': 'pan',
            'phone': '1234',
            'email': 'peter@oaf.oaf',
            'country': 'ug',
            'state': 'kla',
            'village': 'kaz'
        }

        response = self.client.post(
            '/farmers',
            data=json.dumps(body),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_post_farmers_with_bad_data(self):
        """ Test get farmers endpoint """

        response = self.client.post(
            '/farmers',
            content_type='application/json'
        )
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])

    def test_put_farmers(self):
        """ Test get farmers endpoint """
        body = {
            'firstname': 'john',
            'lastname': 'doe',
            'phone': '123',
            'email': 'john@oaf.oaf',
            'country': 'ug',
            'state': 'kla',
            'village': 'kaz'
        }

        response = self.client.put(
            '/farmers/'+ str(self.farmer.id),
            data=json.dumps(body),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_put_farmer_who_does_not_exit(self):
        """ Test get farmers endpoint """
        body = {
            'firstname': 'john',
            'lastname': 'doe',
            'phone': '123',
            'email': 'john@oaf.oaf',
            'country': 'ug',
            'state': 'kla',
            'village': 'kaz'
        }

        response = self.client.put(
            '/farmers/100',
            data=json.dumps(body),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])


    def test_delete_farmer(self):
        """ Test get farmers endpoint """

        response = self.client.delete('/farmers/'+ str(self.farmer.id))
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_farmer_who_does_not_exit(self):
        """ Test get farmers endpoint """
        
        response = self.client.delete('/farmers/100')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])