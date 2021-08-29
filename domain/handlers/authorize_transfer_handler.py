import json
from typing import Any

from domain.enums.transfer_validation_enum import TransferValidationEnum
from domain.handlers.abstract_base_handlers import AbstractHandler
from infra.repositories.url_repository import UrlRepository


class AuthorizeTransferHandler(AbstractHandler):
    url_repository = UrlRepository()

    def handle(self, context: Any) -> TransferValidationEnum:
        request = self.url_repository.make_request(url="https://run.mocky.io/v3/8fafdd68-a090-496f-8c9a-3442cf30dae6",
                                                   method="GET")
        response = request.read()

        authorized = json.loads(response).get("message")

        if authorized == "Autorizado":
            return TransferValidationEnum.authorized
        return TransferValidationEnum.not_authorized
