import unittest
from unittest import mock
from app import app
from app.models.User import User
from flask_login import login_user, logout_user, current_user


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        # Create a test Flask app
        self.client = app.test_client()

    def test_register_user(self):
        with app.app_context():
            # Mock the database operations in user_service.register_user
            with mock.patch('app.services.user_service.User.query') as mock_user_query:
                mock_user_query.filter_by.return_value.first.return_value = None  # User doesn't exist

                with mock.patch('app.services.user_service.db.session') as mock_db_session:
                    # Set the return value for the mock
                    mock_db_session.commit.return_value = None

                    # Make a request to the endpoint
                    response = self.client.post('/api/user/register',
                                                json={'username': 'test_user', 'password': 'password'})

                    # Assert the expected response
                    self.assertEqual(response.status_code, 201)
                    expected_response = {'message': 'User registered successfully', 'user_id': mock.ANY}
                    self.assertEqual(response.get_json(), expected_response)

    def test_login_user(self):
        with app.test_request_context():
            u = User()
            u.id = 1
            u.username = 'test_user'
            u.set_password('test')
            # Mock the database operations in user_service.login
            with mock.patch('app.services.user_service.User.query') as mock_user_query:
                mock_user_query.filter_by.return_value.first.return_value = u
                mock_user_query.filter_by.return_value.first.check_password.return_value = True

                # Make a request to the endpoint
                response = self.client.post('/api/user/login', json={'username': 'test_user', 'password': 'test'})

                # Assert the expected response
                self.assertEqual(response.status_code, 201)
                expected_response = {'message': 'Login successful', 'user_id': 1}
                self.assertEqual(response.get_json(), expected_response)

    def test_user_update(self):
        with app.test_request_context():
            u = User()
            u.id = 1
            u.username = 'test_user'
            u.set_password('test')
            login_user(u)
            # Mock the database operations in user_service.user_update
            with mock.patch('app.models.User.User.query') as mock_user_query:
                mock_user_query.filter_by.return_value.first.return_value = None

                with mock.patch('app.services.user_service.db.session') as mock_db_session:
                    # Set the return value for the mock
                    mock_db_session.commit.return_value = None

                    # Make a request to the endpoint
                    response = self.client.put('/api/user/',
                                               json={'username': 'new_username', 'password': 'new_password'})

                    # Assert the expected response
                    self.assertEqual(response.status_code, 201)
                    expected_response = {'message': 'successfully updated'}
                    self.assertEqual(response.get_json(), expected_response)

            logout_user()

    def test_logout_user(self):
        with app.test_request_context():
            u = User()
            u.id = 1
            u.username = 'test_user'
            u.set_password('test')
            login_user(u)
            # Mock the database operations in user_service.logout

            with mock.patch('app.services.user_service.logout') as mock_logout:
                # Make a request to the endpoint
                response = self.client.post('/api/user/logout')

                # Assert the expected response
                self.assertEqual(response.status_code, 201)
                expected_response = {'message': 'Successfully logged out'}
                self.assertEqual(response.get_json(), expected_response)
            logout_user()

    def test_delete_user(self):
        with app.test_request_context():
            u = User()
            u.id = 1
            u.username = 'test_user'
            u.set_password('test')
            login_user(u)
            # Mock the database operations in user_service.delete_user
            with mock.patch('app.models.User.User.query') as mock_user_query:
                mock_user_query.filter_by.return_value.first.return_value = u

                with mock.patch('app.db.session') as mock_db_session:
                    # Set the return value for the mock
                    # mock_db_session.delete.return_value = None
                    mock_db_session.commit.return_value = None

                    # Make a request to the endpoint

                    response = self.client.delete('/api/user/delete')
                    # Assert the expected response
                    self.assertEqual(response.status_code, 201)
                    expected_response = {'message': 'Deleted'}
                    self.assertEqual(response.get_json(), expected_response)
            logout_user()
