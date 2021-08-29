import uvicorn
from fastapi import FastAPI

from presentation.routers.user_routers import router as user_router
from presentation.routers.wallet_routers import router as wallet_router

app = FastAPI(title="WalletAPI")

app.include_router(
    router=user_router,
    tags=["user"]
)
app.include_router(
    router=wallet_router,
    tags=["wallet"]
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
