from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from domain.models.user_model import UserModel
from domain.services.user_service import UserService
from tests.mock_data import mock_user


class TestUserService(TestCase):
    @patch("domain.services.user_service.WalletRepository")
    @patch("domain.services.user_service.UserRepository")
    def setUp(self, mock_user_repo, mock_wallet_repo) -> None:
        self.user_mock = mock_user()
        self.mock_user_repo = mock_user_repo
        self.mock_wallet_repo = mock_wallet_repo
        self.user_service = UserService()

    def test_get_user(self):
        self.mock_user_repo().get_user.return_value = self.user_mock
        test_case = self.user_service.get_user(user_id=4)
        self.assertIsInstance(test_case, dict)

    def test_insert_user(self):
        self.mock_user_repo().insert_user.return_value = self.user_mock
        self.mock_wallet_repo().insert_wallet.return_value = True

        status_code, message = self.user_service.insert_user(user=UserModel(**self.user_mock))
        self.assertEqual(status_code, 201)

        self.mock_wallet_repo().insert_wallet.return_value = False
        status_code, message = self.user_service.insert_user(user=UserModel(**self.user_mock))
        self.assertEqual(status_code, 201)

        self.mock_user_repo().insert_user.return_value = None
        status_code, message = self.user_service.insert_user(user=UserModel(**self.user_mock))
        self.assertEqual(status_code, 400)
