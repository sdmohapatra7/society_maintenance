import unittest
from unittest.mock import patch, MagicMock
from werkzeug.security import generate_password_hash
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dev3.bl.user_bl import UserBL

class TestUserBL(unittest.TestCase):

    @patch('dev3.bl.user_bl.UserDBH')
    def test_register_existing_user(self, mock_user_dbh):
        # Mock that a user already exists
        mock_user_dbh.get_by_username.return_value = True
        
        success, res = UserBL.register("john", "john@test.com", "pass123")
        
        self.assertFalse(success)
        self.assertEqual(res, "Username already exists")
        mock_user_dbh.create_user.assert_not_called()

    @patch('dev3.bl.user_bl.UserDBH')
    def test_register_new_user(self, mock_user_dbh):
        # Mock that user does not exist
        mock_user_dbh.get_by_username.return_value = None
        
        # Mock the created user object mapping
        mock_created_user = MagicMock()
        mock_created_user._mapping = {"id": 1, "username": "newuser", "role": "resident"}
        mock_user_dbh.create_user.return_value = mock_created_user
        
        success, res = UserBL.register("newuser", "new@test.com", "pass123")
        
        self.assertTrue(success)
        self.assertEqual(res["username"], "newuser")
        self.assertEqual(res["role"], "resident")
        mock_user_dbh.create_user.assert_called_once()

    @patch('dev3.bl.user_bl.UserDBH')
    def test_login_user_not_found(self, mock_user_dbh):
        mock_user_dbh.get_by_username.return_value = None
        
        success, res = UserBL.login("unknown", "pass123")
        
        self.assertFalse(success)
        self.assertEqual(res, "User not found")

    @patch('dev3.bl.user_bl.UserDBH')
    def test_login_invalid_password(self, mock_user_dbh):
        mock_user = MagicMock()
        mock_user.password = generate_password_hash("correctpass")
        mock_user_dbh.get_by_username.return_value = mock_user
        
        success, res = UserBL.login("john", "wrongpass")
        
        self.assertFalse(success)
        self.assertEqual(res, "Invalid credentials")

    @patch('dev3.bl.user_bl.UserDBH')
    def test_login_success(self, mock_user_dbh):
        mock_user = MagicMock()
        mock_user.password = generate_password_hash("correctpass")
        mock_user.is_active = True
        mock_user._mapping = {"id": 1, "username": "john"}
        mock_user_dbh.get_by_username.return_value = mock_user
        
        success, res = UserBL.login("john", "correctpass")
        
        self.assertTrue(success)
        self.assertEqual(res["username"], "john")

if __name__ == '__main__':
    unittest.main()
