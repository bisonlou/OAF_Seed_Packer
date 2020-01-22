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

myApp = Flask(__name__)
myApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database_path = os.environ['TEST_DATABASE_URL']

create_db(myApp, database_path)
farmers_app(myApp)
errorhandler_app(myApp)

class FarmersTestCase(unittest.TestCase):

    def setUp(self):
        self.client = myApp.test_client()

    def test_get_farmers(self):
        """ Test get farmers endpoint """
        response = self.client.get('/farmers')
        body = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])