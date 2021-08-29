from pydantic import BaseModel


class WalletModel(BaseModel):
    wallet_id: int
    user_id: int
    total: float = 0.0
