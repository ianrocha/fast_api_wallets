from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TransactionModel(BaseModel):
    origin_user_id: Optional[int]
    origin_wallet_id: Optional[int]
    destination_wallet_id: Optional[int]
    transaction_type_id: int
    value: float
    operation_date: Optional[datetime] = datetime.now()
