from typing import Any

from domain.enums.transfer_validation_enum import TransferValidationEnum
from domain.handlers.abstract_base_handlers import AbstractHandler


class HasMoneyInWalletHandler(AbstractHandler):
    def handle(self, context: Any) -> TransferValidationEnum:
        origin_user_wallet = context.get("origin_user_wallet")
        transaction_model = context.get("transaction_model")

        if origin_user_wallet.total < transaction_model.value:
            return TransferValidationEnum.no_money_in_wallet
        else:
            return super().handle(context=context)
