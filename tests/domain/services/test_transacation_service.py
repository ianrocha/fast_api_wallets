from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from domain.enums.transfer_validation_enum import TransferValidationEnum
from domain.models.transaction_model import TransactionModel
from domain.models.user_model import UserModel
from domain.models.wallet_model import WalletModel
from domain.services.transaction_service import TransactionService
from tests.mock_data import mock_wallet, mock_transaction_transfer, mock_user, mock_getcode, mock_read_not_authorized, \
    mock_read_authorized


class TestTransactionService(TestCase):
    @patch("domain.services.transaction_service.TransactionRepository", Mock())
    def setUp(self) -> None:
        self.context = {
            "origin_user_wallet": WalletModel(**mock_wallet()),
            "origin_user": UserModel(**mock_user()),
            "transaction_model": TransactionModel(**mock_transaction_transfer())
        }
        # self.mock_url_repo = mock_url_repository
        self.transaction_service = TransactionService()

    def test_validate_transfer_is_shopkeeper_true(self):
        self.context["origin_user"].is_shopkeeper = True
        result = self.transaction_service.validate_transfer(context=self.context)
        self.assertEqual(result, TransferValidationEnum.is_shopkeeper)

    def test_validate_transfer_no_money_in_wallet_true(self):
        self.context["transaction_model"].value = 50000.00
        result = self.transaction_service.validate_transfer(context=self.context)
        self.assertEqual(result, TransferValidationEnum.no_money_in_wallet)

    def test_validate_transfer_authorized_false(self):
        with patch("domain.services.transaction_service.AuthorizeTransferHandler.url_repository",
                   MagicMock(read=mock_read_not_authorized)) as mock:
            mock.make_request.return_value = Mock(read=mock_read_not_authorized)
            result = self.transaction_service.validate_transfer(context=self.context)
            self.assertEqual(result, TransferValidationEnum.not_authorized)

    def test_validate_transfer_authorized_true(self):
        with patch("domain.services.transaction_service.AuthorizeTransferHandler.url_repository",
                   MagicMock(read=mock_read_not_authorized)) as mock:
            mock.make_request.return_value = Mock(read=mock_read_authorized)
            result = self.transaction_service.validate_transfer(context=self.context)
            self.assertEqual(result, TransferValidationEnum.authorized)
