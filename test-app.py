import unittest
from app import app

class TestUserService(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User Service is running!", response.data)

    def test_get_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)

    def test_get_single_user(self):
        response = self.app.get('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Alice Smith')

    def test_get_non_existent_user(self):
        response = self.app.get('/users/99')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"User not found", response.data)

if __name__ == '__main__':
    unittest.main()
