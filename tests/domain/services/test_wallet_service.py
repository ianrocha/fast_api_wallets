from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from domain.enums.transfer_validation_enum import TransferValidationEnum
from domain.models.transaction_model import TransactionModel
from domain.models.user_model import UserModel
from domain.models.wallet_model import WalletModel
from domain.services.user_service import UserService
from domain.services.wallet_service import WalletService
from tests.mock_data import mock_user, mock_wallet, mock_transaction_transfer, mock_getcode


class TestWalletService(TestCase):
    @patch("domain.services.wallet_service.TransactionService")
    @patch("domain.services.wallet_service.UrlRepository")
    @patch("domain.services.wallet_service.UserService")
    @patch("domain.services.wallet_service.WalletRepository")
    def setUp(self, mock_wallet_repo, mock_user_service,
              mock_url_repo, mock_transaction_service) -> None:
        self.mock_user = mock_user()
        self.mock_wallet = mock_wallet()
        self.mock_transaction_transfer = mock_transaction_transfer()

        self.mock_wallet_repo = mock_wallet_repo
        self.mock_user_service = mock_user_service
        self.mock_url_repo = mock_url_repo
        self.mock_transaction_service = mock_transaction_service

        self.wallet_service = WalletService()

    def test_get_user_wallet(self):
        self.mock_wallet_repo().get_user_wallet.return_value = self.mock_wallet
        test_case = self.wallet_service.get_user_wallet(user_id=5)
        self.assertIsInstance(test_case, WalletModel)

    def test_do_transaction_withdraw(self):
        self.mock_wallet_repo().get_user_wallet.return_value = self.mock_wallet
        transaction_model = TransactionModel(transaction_type_id=1, value=100.00)
        status_code, message = self.wallet_service.do_transaction(transaction_model=transaction_model)
        self.assertEqual(status_code, 501)

    def test_do_transaction_deposit(self):
        self.mock_wallet_repo().do_deposit.return_value = True
        self.mock_transaction_service().save_historic.return_value = True
        transaction_model = TransactionModel(destination_wallet_id=5,
                                             transaction_type_id=3,
                                             value=100.00)
        status_code, message = self.wallet_service.do_transaction(transaction_model=transaction_model)
        self.assertEqual(status_code, 201)

        self.mock_wallet_repo().do_deposit.return_value = False
        status_code, message = self.wallet_service.do_transaction(transaction_model=transaction_model)
        self.assertEqual(status_code, 400)

    def test_do_transaction_transfer_is_shopkeeper_true(self):
        self.mock_user["is_shopkeeper"] = True
        self.mock_user_service().get_user.return_value = self.mock_user

        self.mock_wallet_repo().get_user_wallet.return_value = self.mock_wallet
        self.mock_transaction_service().validate_transfer.return_value = TransferValidationEnum.is_shopkeeper

        status_code, message = self.wallet_service.do_transaction(
            transaction_model=TransactionModel(**self.mock_transaction_transfer))
        self.assertEqual(status_code, 412)
        self.assertEqual(message, TransferValidationEnum.is_shopkeeper)
        self.mock_user["is_shopkeeper"] = False

    def test_do_transaction_transfer_has_enough_money_false(self):
        self.mock_user_service().get_user.return_value = self.mock_user

        self.mock_wallet_repo().get_user_wallet.return_value = self.mock_wallet
        self.mock_transaction_service().validate_transfer.return_value = TransferValidationEnum.no_money_in_wallet

        status_code, message = self.wallet_service.do_transaction(
            transaction_model=TransactionModel(**self.mock_transaction_transfer))
        self.assertEqual(status_code, 412)
        self.assertEqual(message, TransferValidationEnum.no_money_in_wallet)

    def test_do_transaction_transfer_authorized_false(self):
        self.mock_user_service().get_user.return_value = self.mock_user

        self.mock_wallet_repo().get_user_wallet.return_value = self.mock_wallet
        self.mock_transaction_service().validate_transfer.return_value = TransferValidationEnum.not_authorized

        status_code, message = self.wallet_service.do_transaction(
            transaction_model=TransactionModel(**self.mock_transaction_transfer))
        self.assertEqual(status_code, 412)
        self.assertEqual(message, TransferValidationEnum.not_authorized)

    def test_do_transaction_transfer_authorized_true(self):
        self.mock_user_service().get_user.return_value = self.mock_user

        self.mock_wallet_repo().get_user_wallet.return_value = self.mock_wallet
        self.mock_transaction_service().validate_transfer.return_value = TransferValidationEnum.authorized
        self.mock_transaction_service().save_historice.return_value = True
        self.mock_url_repo().make_request.return_value = Mock(getcode=mock_getcode)

        status_code, message = self.wallet_service.do_transaction(
            transaction_model=TransactionModel(**self.mock_transaction_transfer))
        self.assertEqual(status_code, 201)
        self.assertEqual(message, TransferValidationEnum.authorized)

    def test_do_transaction_unknown_transaction(self):
        self.mock_user_service().get_user.return_value = self.mock_user

        self.mock_wallet_repo().get_user_wallet.return_value = self.mock_wallet

        status_code, message = self.wallet_service.do_transaction(
            transaction_model=TransactionModel(transaction_type_id=4,
                                               value=150.50))
        self.assertEqual(status_code, 404)
        self.assertEqual(message, TransferValidationEnum.unknown_transaction)

