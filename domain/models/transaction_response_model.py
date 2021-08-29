from pydantic import BaseModel

from domain.models.transaction_model import TransactionModel


class TransactionResponseModel(BaseModel):
    message: str
    transaction_receipt: TransactionModel
