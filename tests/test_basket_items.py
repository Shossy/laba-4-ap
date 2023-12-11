import unittest
from datetime import datetime
from unittest import mock
from app import app
from app.models.BasketItem import BasketItem
from app.models.Product import Product
from app.models.User import User
from flask_login import login_user
from app.services.basket_service import add_item_to_basket, get_basket, remove_item_from_basket, pay_for_order, \
    clear_basket_from_items


class TestBasketEndpoints(unittest.TestCase):

    def setUp(self):
        # Create a test Flask app
        self.client = app.test_client()

    def test_get_basket(self):
        with app.test_request_context():
            u = User()
            u.id = 1
            u.username = 'test_user'
            u.set_password('test')
            login_user(u)
            mock_product = Product(id=1, name="Test Product", description="Test Description", price=10.0, quantity=20)
            bi = BasketItem(id=1, product=mock_product, user_id=1, quantity=5, product_id=1,
                            added_at=datetime(2022, 10, 8))
            with mock.patch('app.routes.baskets.routes.get_basket') as mock_get_basket:
                # Set the return value for the mock
                mock_get_basket.return_value = [bi]

                response = self.client.get('/api/basket/')

                # Assert the expected response
                self.assertEqual(response.status_code, 200)
                expected_response = [{'added_at': '2022-10-08T00:00:00',
                                      'id': 1,
                                      'product': {'description': 'Test Description',
                                                  'id': 1,
                                                  'name': 'Test Product',
                                                  'price': 10.0,
                                                  'quantity': 20},
                                      'product_id': 1,
                                      'quantity': 5,
                                      'user_id': 1}]
                self.assertEqual(response.get_json(), expected_response)

    def test_add_item_to_basket(self):
        with app.test_request_context():
            u = User()
            u.id = 1
            u.username = 'test_user'
            u.set_password('test')
            login_user(u)
            mock_product = Product(id=1, name="Test Product", description="Test Description", price=10.0, quantity=20)
            bi = BasketItem(id=1, product=mock_product, user_id=1, quantity=5, product_id=1,
                            added_at=datetime(2022, 10, 8))
            with mock.patch('app.models.Product.Product.query') as mock_get_product:
                # Set the return value for the mock
                mock_get_product.get.return_value = mock_product
                with mock.patch('app.models.BasketItem.BasketItem.query') as mock_basket_item:
                    # Set the return value for the mock
                    mock_basket_item.filter_by.return_value.first.return_value = bi
                    with mock.patch('app.services.basket_service.db.session') as mock_db_session:
                        # Set the return value for the mock
                        mock_db_session.commit.return_value = None
                        # Make a request to the endpoint
                        response = self.client.post('/api/basket/add_item',
                                                    json={'product_id': 1, 'quantity': 2})

                        # Assert the expected response
                        self.assertEqual(response.status_code, 201)
                        expected_response = {'message': 'Item added to basket successfully'}
                        self.assertEqual(response.get_json(), expected_response)

    def test_remove_item_from_basket(self):
        with app.test_request_context():
            u = User()
            u.id = 1
            u.username = 'test_user'
            u.set_password('test')
            login_user(u)
            mock_product = Product(id=1, name="Test Product", description="Test Description", price=10.0, quantity=20)
            bi = BasketItem(id=1, product=mock_product, user_id=1, quantity=5, product_id=1,
                            added_at=datetime(2022, 10, 8))
            with mock.patch('app.models.Product.Product.query') as mock_get_product:
                # Set the return value for the mock
                mock_get_product.get.return_value = mock_product

                with mock.patch('app.models.BasketItem.BasketItem.query') as mock_basket_item:
                    # Set the return value for the mock
                    mock_basket_item.filter_by.return_value.first.return_value = bi
                    with mock.patch('app.services.basket_service.db.session') as mock_db_session:
                        # Set the return value for the mock
                        mock_db_session.commit.return_value = None

                        # Make a request to the endpoint
                        response = self.client.post('/api/basket/remove_item',
                                                    json={'product_id': 1, 'quantity': 2})

                        # Assert the expected response
                        self.assertEqual(response.status_code, 201)
                        expected_response = {'message': 'Items removed from basket successfully'}
                        self.assertEqual(response.get_json(), expected_response)

    def test_pay_for_order(self):
        with app.test_request_context():
            u = User()
            u.id = 1
            u.username = 'test_user'
            u.set_password('test')
            login_user(u)
            mock_product = Product(id=1, name="Test Product", description="Test Description", price=10.0, quantity=20)
            bi = BasketItem(id=1, product=mock_product, user_id=1, quantity=5, product_id=1,
                            added_at=datetime(2022, 10, 8))
            with mock.patch('app.routes.baskets.routes.get_basket') as mock_get_basket:
                # Set the return value for the mock
                mock_get_basket.return_value = [bi]
                with mock.patch('app.services.basket_service.db.session') as mock_db_session:
                    # Set the return value for the mock
                    mock_db_session.commit.return_value = None

                    # Make a request to the endpoint
                    response = self.client.post('/api/basket/pay')

                    # Assert the expected response
                    self.assertEqual(response.status_code, 201)
                    expected_response = {'message': 'Payment done successfully'}
                    self.assertEqual(response.get_json(), expected_response)

    def test_clear_basket(self):
        with app.test_request_context():
            u = User()
            u.id = 1
            u.username = 'test_user'
            u.set_password('test')
            login_user(u)

            with mock.patch('app.services.basket_service.db.session') as mock_db_session:
                # Set the return value for the mock
                mock_db_session.commit.return_value = None

                # Make a request to the endpoint
                response = self.client.delete('/api/basket/clear_basket')

                # Assert the expected response
                self.assertEqual(response.status_code, 201)
                expected_response = {'message': 'Cleared successfully'}
                self.assertEqual(response.get_json(), expected_response)
