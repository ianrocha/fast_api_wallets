from domain.enums.transfer_validation_enum import TransferValidationEnum
from domain.handlers.authorize_transfer_handler import AuthorizeTransferHandler
from domain.handlers.has_money_in_wallet_handler import HasMoneyInWalletHandler
from domain.handlers.is_shopkeeper_handler import IsShopkeeperHandler
from domain.models.transaction_model import TransactionModel
from infra.repositories.transaction_repository import TransactionRepository


class TransactionService:
    def __init__(self):
        self.is_shopkeeper_handler = IsShopkeeperHandler()
        self.has_money_in_wallet_handler = HasMoneyInWalletHandler()
        self.authorize_transfer_handler = AuthorizeTransferHandler()

        self.is_shopkeeper_handler.set_next(self.has_money_in_wallet_handler).\
            set_next(self.authorize_transfer_handler)

        self.transaction_repository = TransactionRepository()

    def validate_transfer(self, context: dict) -> TransferValidationEnum:
        result = self.is_shopkeeper_handler.handle(context=context)
        return result

    def save_historic(self, transaction_model: TransactionModel) -> bool:
        return self.transaction_repository.save_historic(transaction_model=transaction_model)
