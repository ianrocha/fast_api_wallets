from fastapi import APIRouter
from fastapi.responses import JSONResponse

from domain.models.message_response_model import MessageResponseModel
from domain.models.transaction_model import TransactionModel
from domain.models.transaction_response_model import TransactionResponseModel
from domain.models.wallet_model import WalletModel
from domain.services.wallet_service import WalletService

router = APIRouter(
    prefix="/wallet"
)

wallet_service = WalletService()


@router.get("/{user_id}",
            response_model=WalletModel)
def get_user_wallet(user_id: int):
    return wallet_service.get_user_wallet(user_id=user_id)


@router.post("/transaction",
             response_model=TransactionResponseModel,
             responses={
                 201: {"model": TransactionResponseModel, "description": "Transaction Made Successfully"},
                 400: {"model": MessageResponseModel, "description": "Transaction Failed"},
                 412: {"model": MessageResponseModel, "description": "Validation Error"},
                 404: {"model": MessageResponseModel, "description": "Transaction Not Found"},
                 501: {"model": MessageResponseModel, "description": "Not Implemented Yet"},
             })
def do_wallet_transaction(transaction_model: TransactionModel = None):
    status_code, message = wallet_service.do_transaction(transaction_model=transaction_model)
    if status_code == 201:
        return JSONResponse(status_code=status_code, content={"message": message,
                                                              "transaction_receipt": transaction_model.json()})
    else:
        return JSONResponse(status_code=status_code, content={"message": message})
