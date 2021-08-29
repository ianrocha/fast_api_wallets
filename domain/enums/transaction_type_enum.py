from enum import IntEnum


class TransactionTypeEnum(IntEnum):
    transaction_unknown = 0
    withdraw = 1
    transfer = 2
    deposit = 3
