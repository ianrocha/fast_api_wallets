from domain.dtos.user_dto import UserDto
from domain.models.user_model import UserModel
from infra.repositories.user_repository import UserRepository
from infra.repositories.wallet_repository import WalletRepository


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.wallet_repository = WalletRepository()

    def get_user(self, user_id: int) -> dict:
        result = UserDto(self.user_repository.get_user(user_id=user_id))
        return result

    def insert_user(self, user: UserModel):
        last_inserted_id = self.user_repository.insert_user(user=user)
        if last_inserted_id:
            result = self.wallet_repository.insert_wallet(user_id=last_inserted_id)
            if result:
                return 201, "User and Wallet Created Successfully!"
            else:
                return 201, "User Created Successfully! But there was a problem creating the wallet"
        return 400, "Something went wrong creating user!"

    def inactivate_user(self, user_id: int) -> bool:
        return self.user_repository.inactivate_user(user_id=user_id)
