from enum import Enum


class TransferValidationEnum(str, Enum):
    is_shopkeeper = "is_shopkeeper"
    no_money_in_wallet = "no_money_in_wallet"
    not_authorized = "not_authorized"
    authorized = "authorized"
    unknown_transaction = "transaction not recognized or missing information"
