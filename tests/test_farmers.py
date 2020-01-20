import unittest
from os import environ
from functools import wraps
from unittest.mock import patch

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

from api.models.farmer import Farmer
from api.database import create_db
from api import app


class TestFarmers(unittest.TestCase):
  
    def setUp(self):
        self.app = app
        self.databse_uri = environ.get('TEST_DATABASE_URL', None)
        create_db(self.app, self.databse_uri)
        self.client = self.app.test_client

        sample_farmer = Farmer(
            firstname = 'john',
            lastname = 'doe',
            phone = '0765667675',
            email = 'johndoe@gmail.com',
            country = 'uganda',
            state = 'kampala',
            village = 'kazing'
        )

    def test_get_farmers(self):
        response = self.client().get('/farmers')
        data = response.get_json()
        print(data)
        self.assertTrue(data['success'])


