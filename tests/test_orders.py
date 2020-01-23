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
patch('api.controllers.orders.requires_auth', mock_func).start()
from api.controllers.orders import orders_app
from api.models.order import Order
from api.models.farmer import Farmer
from api.models.product import Product
from api.database import db

myApp = Flask(__name__)
myApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database_path = os.environ['TEST_DATABASE_URL']

create_db(myApp, database_path)
orders_app(myApp)
errorhandler_app(myApp)

class FarmersTestCase(unittest.TestCase):

    def setUp(self):
        self.client = myApp.test_client()
        db.create_all()
        
        db.session.add(
            Product(
            name='lentils',
            description='lentils',
            qty=100,
            units='kgs',
            unit_price= 1200
            )
        )

        db.session.add(
            Farmer(
            firstname='jack',
            lastname='sparrow',
            phone='123123',
            email='jack@oaf.oaf',
            country= 'ug',
            state='kla',
            village='kaz'
            )
        )

        db.session.commit()
        db.session.close()

        self.product = Product.query.first()
        self.farmer = Farmer.query.first()

        db.session.add(
            Order(
            farmer_id=self.farmer.id,
            order_date='2020-01-01'
            )
        )
        db.session.commit()
        db.session.close()

        self.order = Order.query.first()
        

    def tearDown(self):
        db.drop_all()

    def test_get_orders(self):
        """ Test get orders endpoint """
        response = self.client.get('/orders')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']), 1)

    def test_get_orders_with_wrong_method(self):
        """
        Test get order endpoint
        with wrong method
        Expect 405
        """
        response = self.client.put('/orders')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 405)
        self.assertFalse(data['success'])

    def test_get_orders_with_wrong_endpoint(self):
        """
        Test get orders endpoint
        With wrong endpoint
        Expect 404
        """
        response = self.client.get('/orderss')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        
    def test_post_order(self):
        """
        Test post order endpoint
        Expect 200
        """
        body = {
            'farmer_id': 1,
            'order_date': '2020-01-01',
            'order_details': [
                {
                    'product_id': 1,
                    'line_no': 1,
                    'order_qty': 10,
                    'line_total': 10000
                }
            ]
        }

        response = self.client.post(
            '/orders',
            data=json.dumps(body),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_post_orders_with_bad_data(self):
        """
        Test post orders endpoint
        Without data
        Expect 400
        """

        response = self.client.post(
            '/orders',
            content_type='application/json'
        )
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])


    def test_delete_order(self):
        """
        Test delete orders endpoint
        Expect 200
        """

        response = self.client.delete('/orders/'+ str(self.order.id))
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_order_which_does_not_exit(self):
        """
        Test delete order endpoint
        With non-existent order
        Expect 404
        """
        
        response = self.client.delete('/orders/100')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])