from typing import Optional, ClassVar

from pydantic import BaseModel


class UserModel(BaseModel):
    user_id: Optional[int]
    name: str
    document: str
    email: str
    password: str
    is_shopkeeper: bool
    is_active: Optional[bool] = True
