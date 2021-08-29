from domain.enums.transaction_type_enum import TransactionTypeEnum
from domain.enums.transfer_validation_enum import TransferValidationEnum
from domain.models.transaction_model import TransactionModel
from domain.models.user_model import UserModel
from domain.models.wallet_model import WalletModel
from domain.services.transaction_service import TransactionService
from domain.services.user_service import UserService
from infra.repositories.url_repository import UrlRepository
from infra.repositories.wallet_repository import WalletRepository


class WalletService:
    def __init__(self):
        self.wallet_repository = WalletRepository()
        self.transaction_service = TransactionService()
        self.user_service = UserService()
        self.url_repository = UrlRepository()

    def get_user_wallet(self, user_id: int) -> WalletModel:
        return WalletModel(**self.wallet_repository.get_user_wallet(user_id=user_id))

    def insert_wallet(self, user_id: int):
        return self.wallet_repository.insert_wallet(user_id=user_id)

    def do_transaction(self, transaction_model: TransactionModel) -> (int, str):
        if transaction_model.transaction_type_id == TransactionTypeEnum.withdraw:

            return 501, "Not Implemented Yet"

        elif transaction_model.transaction_type_id == TransactionTypeEnum.deposit:

            result = self.wallet_repository.do_deposit(transaction_model=transaction_model)
            if result:
                self.notify_destination()
                self.transaction_service.save_historic(transaction_model=transaction_model)
                return 201, "Deposit made successfully!"
            else:
                return 400, "Something went wrong with the deposit!"

        elif transaction_model.transaction_type_id == TransactionTypeEnum.transfer and transaction_model:
            context = {
                "origin_user_wallet": self.get_user_wallet(user_id=transaction_model.origin_user_id),
                "origin_user": UserModel(**self.user_service.get_user(user_id=transaction_model.origin_user_id)),
                "transaction_model": transaction_model
            }

            valid_transaction = self.transaction_service.validate_transfer(context=context)

            if valid_transaction == TransferValidationEnum.authorized:
                result = self.wallet_repository.do_transfer(transaction_model=transaction_model)

                if result:
                    self.notify_destination()
                    self.transaction_service.save_historic(transaction_model=transaction_model)
                return 201, valid_transaction.value
            else:
                return 412, valid_transaction.value

        return 404, TransferValidationEnum.unknown_transaction

    def notify_destination(self):
        response = self.url_repository.make_request(url="http://o4d9z.mocklab.io/notify",
                                                    method="POST")
        return_code = response.getcode()
        if return_code == 201:
            return True
        return False
