from fastapi import APIRouter
from fastapi.responses import JSONResponse

from domain.models.message_response_model import MessageResponseModel
from domain.models.user_model import UserModel
from domain.services.user_service import UserService

router = APIRouter(
    prefix="/user"
)

user_service = UserService()


@router.get("/{user_id}")
def get_user(user_id: int):
    return user_service.get_user(user_id=user_id)


@router.post("/",
             responses={
                 201: {"model": MessageResponseModel, "description": "User Created Successfully"},
                 400: {"model": MessageResponseModel, "description": "Create User Failed"},
             }
             )
def insert_user(user: UserModel):
    status_code, message = user_service.insert_user(user=user)
    return JSONResponse(status_code=status_code, content={"message": message})


@router.delete("/{user_id}")
def inactivate_user(user_id: int):
    result = user_service.inactivate_user(user_id=user_id)
    if result:
        return {"message": "User inactivated"}
    else:
        return {"message": "User could not be inactivated"}
