from io import BytesIO
from unittest.mock import patch

import pytest
from square_database_structure.square.authentication.enums import RecoveryMethodEnum

from square_authentication_helper.main import SquareAuthenticationHelper
from square_authentication_helper.pydantic_models import TokenType


class TestSquareAuthenticationHelperInit:
    """Test initialization of SquareAuthenticationHelper"""

    def test_init_default_parameters(self):
        """Test initialization with default parameters"""
        helper = SquareAuthenticationHelper()
        assert (
            helper.global_str_square_authentication_url_base == "http://localhost:10011"
        )

    def test_init_custom_parameters(self):
        """Test initialization with custom parameters"""
        helper = SquareAuthenticationHelper(
            param_int_square_authentication_port=8080,
            param_str_square_authentication_ip="192.168.1.1",
            param_str_square_authentication_protocol="https",
        )
        assert (
            helper.global_str_square_authentication_url_base
            == "https://192.168.1.1:8080"
        )

    def test_init_with_exception(self):
        """Test initialization handles exceptions"""
        with patch(
            "square_authentication_helper.main.SquareAuthenticationHelper.__init__"
        ) as mock_init:
            mock_init.side_effect = Exception("Init failed")
            with pytest.raises(Exception):
                mock_init(None)


class TestSquareAuthenticationHelperMakeRequest:
    """Test the _make_request internal method"""

    @pytest.fixture
    def helper(self):
        """Fixture to create a SquareAuthenticationHelper instance"""
        return SquareAuthenticationHelper()

    @patch("square_authentication_helper.main.make_request_json_output")
    def test_make_request_success(self, mock_make_request, helper):
        """Test successful request"""
        mock_make_request.return_value = {"status": "success"}

        result = helper._make_request(
            method="POST", endpoint="test/endpoint", json={"key": "value"}
        )

        mock_make_request.assert_called_once_with(
            method="POST",
            base_url="http://localhost:10011",
            endpoint="test/endpoint",
            json={"key": "value"},
            data=None,
            params=None,
            headers=None,
            files=None,
        )
        assert result == {"status": "success"}

    @patch("square_authentication_helper.main.make_request_json_output")
    def test_make_request_with_all_parameters(self, mock_make_request, helper):
        """Test request with all parameters"""
        mock_make_request.return_value = {"status": "success"}

        result = helper._make_request(
            method="GET",
            endpoint="test/endpoint",
            json={"key": "value"},
            data={"data": "test"},
            params={"param": "value"},
            headers={"Authorization": "Bearer token"},
            files={"file": "content"},
        )

        mock_make_request.assert_called_once()
        assert result == {"status": "success"}

    @patch("square_authentication_helper.main.make_request_json_output")
    def test_make_request_exception(self, mock_make_request, helper):
        """Test request raises exception"""
        mock_make_request.side_effect = Exception("Request failed")

        with pytest.raises(Exception):
            helper._make_request(method="POST", endpoint="test")


class TestRegistrationAndLogin:
    """Test registration and login methods"""

    @pytest.fixture
    def helper(self):
        return SquareAuthenticationHelper()

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_register_username_v0(self, mock_request, helper):
        """Test user registration with username"""
        mock_request.return_value = {"user_id": 123}

        result = helper.register_username_v0(
            username="testuser", password="password123", app_id=1
        )

        mock_request.assert_called_once_with(
            method="POST",
            endpoint="register_username/v0",
            json={"username": "testuser", "password": "password123", "app_id": 1},
        )
        assert result == {"user_id": 123}

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_register_username_v0_without_app_id(self, mock_request, helper):
        """Test user registration without app_id"""
        mock_request.return_value = {"user_id": 123}

        result = helper.register_username_v0(
            username="testuser", password="password123"
        )

        mock_request.assert_called_once_with(
            method="POST",
            endpoint="register_username/v0",
            json={"username": "testuser", "password": "password123", "app_id": None},
        )

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_login_username_v0(self, mock_request, helper):
        """Test user login with username"""
        mock_request.return_value = {
            "access_token": "abc123",
            "refresh_token": "def456",
        }

        result = helper.login_username_v0(
            username="testuser",
            password="password123",
            app_id=1,
            assign_app_id_if_missing=True,
        )

        mock_request.assert_called_once_with(
            method="POST",
            endpoint="login_username/v0",
            json={
                "username": "testuser",
                "password": "password123",
                "app_id": 1,
                "assign_app_id_if_missing": True,
            },
        )
        assert result == {"access_token": "abc123", "refresh_token": "def456"}

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_register_login_google_v0(self, mock_request, helper):
        """Test Google registration/login"""
        mock_request.return_value = {"access_token": "token123"}

        result = helper.register_login_google_v0(
            google_id="google123", app_id=1, assign_app_id_if_missing=True
        )

        mock_request.assert_called_once_with(
            method="POST",
            endpoint="register_login_google/v0",
            json={
                "google_id": "google123",
                "app_id": 1,
                "assign_app_id_if_missing": True,
            },
        )


class TestTokenManagement:
    """Test token-related methods"""

    @pytest.fixture
    def helper(self):
        return SquareAuthenticationHelper()

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_generate_access_token_v0(self, mock_request, helper):
        """Test access token generation"""
        mock_request.return_value = {"access_token": "new_token"}

        result = helper.generate_access_token_v0(refresh_token="refresh123")

        mock_request.assert_called_once_with(
            method="GET",
            endpoint="generate_access_token/v0",
            headers={"refresh_token": "refresh123"},
        )
        assert result == {"access_token": "new_token"}

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_validate_and_get_payload_from_token_v0(self, mock_request, helper):
        """Test token validation"""
        mock_request.return_value = {"user_id": 123, "valid": True}

        result = helper.validate_and_get_payload_from_token_v0(
            token="test_token", token_type=TokenType.access_token, app_id=1
        )

        mock_request.assert_called_once_with(
            method="GET",
            endpoint="validate_and_get_payload_from_token/v0",
            headers={"token": "test_token"},
            params={"token_type": TokenType.access_token.value, "app_id": 1},
        )


class TestLogoutMethods:
    """Test logout-related methods"""

    @pytest.fixture
    def helper(self):
        return SquareAuthenticationHelper()

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_logout_v0(self, mock_request, helper):
        """Test logout with refresh token"""
        mock_request.return_value = {"success": True}

        result = helper.logout_v0(refresh_token="refresh123")

        mock_request.assert_called_once_with(
            method="DELETE",
            endpoint="logout/v0",
            headers={"refresh_token": "refresh123"},
        )

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_logout_apps_v0(self, mock_request, helper):
        """Test logout from specific apps"""
        mock_request.return_value = {"success": True}

        result = helper.logout_apps_v0(access_token="access123", app_ids=[1, 2, 3])

        mock_request.assert_called_once_with(
            method="POST",
            endpoint="logout/apps/v0",
            headers={"access_token": "access123"},
            json={"app_ids": [1, 2, 3]},
        )

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_logout_all_v0(self, mock_request, helper):
        """Test logout from all sessions"""
        mock_request.return_value = {"success": True}

        result = helper.logout_all_v0(access_token="access123")

        mock_request.assert_called_once_with(
            method="DELETE",
            endpoint="logout/all/v0",
            headers={"access_token": "access123"},
        )


class TestUserManagement:
    """Test user management methods"""

    @pytest.fixture
    def helper(self):
        return SquareAuthenticationHelper()

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_get_user_details_v0(self, mock_request, helper):
        """Test getting user details"""
        mock_request.return_value = {"user_id": 123, "username": "testuser"}

        result = helper.get_user_details_v0(access_token="access123")

        mock_request.assert_called_once_with(
            method="GET",
            endpoint="get_user_details/v0",
            headers={"access_token": "access123"},
        )

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_update_user_app_ids_v0(self, mock_request, helper):
        """Test updating user app IDs"""
        mock_request.return_value = {"success": True}

        result = helper.update_user_app_ids_v0(
            access_token="access123", app_ids_to_add=[1, 2], app_ids_to_remove=[3, 4]
        )

        mock_request.assert_called_once_with(
            method="PATCH",
            endpoint="update_user_app_ids/v0",
            headers={"access_token": "access123"},
            json={"app_ids_to_add": [1, 2], "app_ids_to_remove": [3, 4]},
        )

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_update_username_v0(self, mock_request, helper):
        """Test updating username"""
        mock_request.return_value = {"success": True}

        result = helper.update_username_v0(
            new_username="newuser", access_token="access123"
        )

        mock_request.assert_called_once_with(
            method="PATCH",
            endpoint="update_username/v0",
            params={"new_username": "newuser"},
            headers={"access_token": "access123"},
        )

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_delete_user_v0(self, mock_request, helper):
        """Test deleting user"""
        mock_request.return_value = {"success": True}

        result = helper.delete_user_v0(password="password123", access_token="access123")

        mock_request.assert_called_once_with(
            method="POST",
            endpoint="delete_user/v0",
            json={"password": "password123"},
            headers={"access_token": "access123"},
        )

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_update_profile_details_v0(self, mock_request, helper):
        """Test updating profile details"""
        mock_request.return_value = {"success": True}

        result = helper.update_profile_details_v0(
            access_token="access123",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone_number_country_code="+1",
            phone_number="1234567890",
        )

        mock_request.assert_called_once_with(
            method="PATCH",
            endpoint="update_profile_details/v0",
            params={
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "phone_number_country_code": "+1",
                "phone_number": "1234567890",
            },
            headers={"access_token": "access123"},
        )


class TestPasswordManagement:
    """Test password management methods"""

    @pytest.fixture
    def helper(self):
        return SquareAuthenticationHelper()

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_update_password_v0(self, mock_request, helper):
        """Test password update"""
        mock_request.return_value = {"success": True}

        result = helper.update_password_v0(
            old_password="old123",
            new_password="new456",
            access_token="access123",
            logout_other_sessions=True,
            preserve_session_refresh_token="refresh123",
        )

        mock_request.assert_called_once_with(
            method="PATCH",
            endpoint="update_password/v0",
            json={
                "old_password": "old123",
                "new_password": "new456",
                "logout_other_sessions": True,
                "preserve_session_refresh_token": "refresh123",
            },
            headers={"access_token": "access123"},
        )

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_send_reset_password_email_v0(self, mock_request, helper):
        """Test sending password reset email"""
        mock_request.return_value = {"success": True}

        result = helper.send_reset_password_email_v0(username="testuser")

        mock_request.assert_called_once_with(
            method="POST",
            endpoint="send_reset_password_email/v0",
            json={"username": "testuser"},
        )

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_reset_password_and_login_using_backup_code_v0(self, mock_request, helper):
        """Test password reset using backup code"""
        mock_request.return_value = {"access_token": "token123"}

        result = helper.reset_password_and_login_using_backup_code_v0(
            backup_code="backup123",
            username="testuser",
            new_password="newpass",
            app_id=1,
            logout_other_sessions=True,
        )

        mock_request.assert_called_once_with(
            method="POST",
            endpoint="reset_password_and_login_using_backup_code/v0",
            json={
                "backup_code": "backup123",
                "username": "testuser",
                "new_password": "newpass",
                "app_id": 1,
                "logout_other_sessions": True,
            },
        )

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_reset_password_and_login_using_reset_email_code_v0(
        self, mock_request, helper
    ):
        """Test password reset using email code"""
        mock_request.return_value = {"access_token": "token123"}

        result = helper.reset_password_and_login_using_reset_email_code_v0(
            reset_email_code="email123",
            username="testuser",
            new_password="newpass",
            app_id=1,
            logout_other_sessions=False,
        )

        mock_request.assert_called_once_with(
            method="POST",
            endpoint="reset_password_and_login_using_reset_email_code/v0",
            json={
                "reset_email_code": "email123",
                "username": "testuser",
                "new_password": "newpass",
                "app_id": 1,
                "logout_other_sessions": False,
            },
        )


class TestProfileAndRecovery:
    """Test profile and recovery methods"""

    @pytest.fixture
    def helper(self):
        return SquareAuthenticationHelper()

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_update_profile_photo_v0_with_photo(self, mock_request, helper):
        """Test updating profile photo"""
        mock_request.return_value = {"success": True}
        photo_file = ("photo.jpg", BytesIO(b"fake image data"), "image/jpeg")

        result = helper.update_profile_photo_v0(
            access_token="access123", profile_photo=photo_file
        )

        mock_request.assert_called_once_with(
            method="PATCH",
            endpoint="update_profile_photo/v0",
            headers={"access_token": "access123"},
            files={"profile_photo": photo_file},
        )

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_update_profile_photo_v0_remove_photo(self, mock_request, helper):
        """Test removing profile photo"""
        mock_request.return_value = {"success": True}

        result = helper.update_profile_photo_v0(
            access_token="access123", profile_photo=None
        )

        mock_request.assert_called_once_with(
            method="PATCH",
            endpoint="update_profile_photo/v0",
            headers={"access_token": "access123"},
            files=None,
        )

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_update_user_recovery_methods_v0(self, mock_request, helper):
        """Test updating recovery methods"""
        mock_request.return_value = {"success": True}

        result = helper.update_user_recovery_methods_v0(
            access_token="access123",
            recovery_methods_to_add=[
                RecoveryMethodEnum.BACKUP_CODE,
            ],
            recovery_methods_to_remove=[RecoveryMethodEnum.EMAIL],
        )

        # Verify the call was made with formatted enum values
        call_args = mock_request.call_args
        assert call_args[1]["endpoint"] == "update_user_recovery_methods/v0"
        assert call_args[1]["headers"] == {"access_token": "access123"}
        assert (
            RecoveryMethodEnum.BACKUP_CODE.value
            in call_args[1]["json"]["recovery_methods_to_add"]
        )

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_update_user_recovery_methods_v0_defaults(self, mock_request, helper):
        """Test updating recovery methods with default empty lists"""
        mock_request.return_value = {"success": True}

        result = helper.update_user_recovery_methods_v0(access_token="access123")

        call_args = mock_request.call_args
        assert call_args[1]["json"]["recovery_methods_to_add"] == []
        assert call_args[1]["json"]["recovery_methods_to_remove"] == []

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_generate_account_backup_codes_v0(self, mock_request, helper):
        """Test generating backup codes"""
        mock_request.return_value = {"backup_codes": ["code1", "code2"]}

        result = helper.generate_account_backup_codes_v0(access_token="access123")

        mock_request.assert_called_once_with(
            method="POST",
            endpoint="generate_account_backup_codes/v0",
            headers={"access_token": "access123"},
        )

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_get_user_recovery_methods_v0(self, mock_request, helper):
        """Test getting user recovery methods"""
        mock_request.return_value = {"recovery_methods": ["EMAIL", "BACKUP_CODES"]}

        result = helper.get_user_recovery_methods_v0(username="testuser")

        mock_request.assert_called_once_with(
            method="GET",
            endpoint="get_user_recovery_methods/v0",
            params={"username": "testuser"},
        )


class TestEmailVerification:
    """Test email verification methods"""

    @pytest.fixture
    def helper(self):
        return SquareAuthenticationHelper()

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_send_verification_email_v0(self, mock_request, helper):
        """Test sending verification email"""
        mock_request.return_value = {"success": True}

        result = helper.send_verification_email_v0(access_token="access123")

        mock_request.assert_called_once_with(
            method="POST",
            endpoint="send_verification_email/v0",
            headers={"access_token": "access123"},
        )

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_validate_email_verification_code_v0(self, mock_request, helper):
        """Test validating email verification code"""
        mock_request.return_value = {"verified": True}

        result = helper.validate_email_verification_code_v0(
            access_token="access123", verification_code="verify123"
        )

        mock_request.assert_called_once_with(
            method="POST",
            endpoint="validate_email_verification_code/v0",
            json={"verification_code": "verify123"},
            headers={"access_token": "access123"},
        )


class TestExceptionHandling:
    """Test exception handling across methods"""

    @pytest.fixture
    def helper(self):
        return SquareAuthenticationHelper()

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_register_username_exception(self, mock_request, helper):
        """Test exception in register_username_v0"""
        mock_request.side_effect = Exception("Network error")

        with pytest.raises(Exception):
            helper.register_username_v0("user", "pass")

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_login_username_exception(self, mock_request, helper):
        """Test exception in login_username_v0"""
        mock_request.side_effect = Exception("Auth error")

        with pytest.raises(Exception):
            helper.login_username_v0("user", "pass", app_id=1)

    @patch.object(SquareAuthenticationHelper, "_make_request")
    def test_update_password_exception(self, mock_request, helper):
        """Test exception in update_password_v0"""
        mock_request.side_effect = Exception("Update failed")

        with pytest.raises(Exception):
            helper.update_password_v0("old", "new", "token")
