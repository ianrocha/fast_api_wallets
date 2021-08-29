from typing import Any

from domain.enums.transfer_validation_enum import TransferValidationEnum
from domain.handlers.abstract_base_handlers import AbstractHandler


class IsShopkeeperHandler(AbstractHandler):
    def handle(self, context: Any) -> TransferValidationEnum:
        origin_user = context.get("origin_user")

        if origin_user.is_shopkeeper:
            return TransferValidationEnum.is_shopkeeper
        else:
            return super().handle(context=context)
