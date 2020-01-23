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
patch('api.controllers.products.requires_auth', mock_func).start()
from api.controllers.products import products_app
from api.models.product import Product
from api.database import db

myApp = Flask(__name__)
myApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database_path = os.environ['TEST_DATABASE_URL']

create_db(myApp, database_path)
products_app(myApp)
errorhandler_app(myApp)

class FarmersTestCase(unittest.TestCase):

    def setUp(self):
        self.client = myApp.test_client()
        db.create_all()

        db.session.add(
            Product(
            name='beans',
            description='beans',
            qty=100,
            units='kgs',
            unit_price= 1200
            )
        )

        db.session.commit()
        self.product = Product.query.first()
        db.session.close()

    def tearDown(self):
        db.drop_all()

    def test_get_products(self):
        """ Test get products endpoint """
        response = self.client.get('/products')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']), 1)

    def test_get_products_with_wrong_method(self):
        """
        Test get products endpoint
        with wrong method
        Expect 405
        """
        response = self.client.put('/products')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 405)
        self.assertFalse(data['success'])

    def test_get_products_with_wrong_endpoint(self):
        """
        Test get products endpoint
        With wrong endpoint
        Expect 404
        """
        response = self.client.get('/productss')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        
    def test_post_product(self):
        """
        Test post product endpoint
        Expect 200
        """
        body = {
            'name': 'cumin',
            'description': 'cumin',
            'qty': 100,
            'units': 'kgs',
            'unit_price': 1000
        }

        response = self.client.post(
            '/products',
            data=json.dumps(body),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_post_products_with_bad_data(self):
        """
        Test post products endpoint
        Without data
        Expect 400
        """

        response = self.client.post(
            '/products',
            content_type='application/json'
        )
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])

    def test_put_products(self):
        """ 
        Test put products endpoint
        Expect 200
        """
        body = {
            'name': 'beans',
            'description': 'bean seeds',
            'qty': 100,
            'units': 'kgs',
            'unit_price': 1000
        }
        response = self.client.put(
            '/products/'+ str(self.product.id),
            data=json.dumps(body),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_put_product_who_does_not_exit(self):
        """
        Test put products endpoint
        With non-existent product
        Expect 404
        """
        body = {
            'name': 'cumin',
            'description': 'cumin',
            'qty': 100,
            'units': 'kgs',
            'unit_price': 1000
        }

        response = self.client.put(
            '/products/100',
            data=json.dumps(body),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])


    def test_delete_product(self):
        """
        Test delete products endpoint
        Expect 200
        """

        response = self.client.delete('/products/'+ str(self.product.id))
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_product_which_does_not_exit(self):
        """
        Test delete product endpoint
        With non-existent product
        Expect 404
        """
        
        response = self.client.delete('/products/100')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])