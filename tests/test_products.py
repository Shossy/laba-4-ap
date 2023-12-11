import unittest
from unittest import mock
from app import app
from app.models.Product import Product


class TestProductEndpoints(unittest.TestCase):

    def setUp(self):
        # Create a test Flask app
        self.client = app.test_client()

    def test_get_products(self):
        with app.test_request_context():
            # Mock the Product.query.all() method
            with mock.patch('app.models.Product.Product.query') as mock_query_all:
                # Set the return value for the mock
                mock_query_all.all.return_value = [
                    Product(id=1, name='Product 1', price=19.99, quantity=50),
                    Product(id=2, name='Product 2', price=29.99, quantity=50),
                ]

                # Make a request to the endpoint
                response = self.client.get('/api/products/')
                # Assert the expected response
                self.assertEqual(response.status_code, 200)
                expected_response = {
                    'products': [
                        {'id': 1, 'name': 'Product 1', 'price': 19.99, 'quantity': 50, 'description': None},
                        {'id': 2, 'name': 'Product 2', 'price': 29.99, 'quantity': 50, 'description': None},
                    ]
                }

                self.assertEqual(response.get_json(), expected_response)

    def test_get_product(self):
        with app.test_request_context():
            # Mock the Product.query.where().first() method
            with mock.patch('app.models.Product.Product.query') as mock_query_first:
                # Set the return value for the mock
                mock_query_first.where().first.return_value = Product(id=1, name='Product 1', price=19.99, quantity=50,
                                                                      description='1')

                # Make a request to the endpoint
                response = self.client.get('/api/products/2/')

                # Assert the expected response
                self.assertEqual(response.status_code, 200)
                expected_response = {'id': 1, 'name': 'Product 1', 'price': 19.99, 'quantity': 50, 'description': '1'}
                self.assertEqual(response.json, expected_response)

    def test_get_product_not_found(self):
        with app.test_request_context():
            # Mock the Product.query.where().first() method to return None
            with mock.patch('app.models.Product.Product.query') as mock_query_first:
                mock_query_first.where().first.return_value = None

                # Make a request to the endpoint
                response = self.client.get('/api/products/999/')
                # Assert the expected response for a not found product
                self.assertEqual(response.status_code, 404)
                expected_response = {'message': 'Product not found'}
                self.assertEqual(response.json, expected_response)



