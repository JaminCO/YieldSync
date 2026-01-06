from fastapi import FastAPI
from app.core.config import settings
from app.api.users import router as user_router
from app.api.wallets import router as wallet_router
from app.api.pools import router as pool_router
from app.db import engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "env": settings.ENV}

# @app.on_event("startup")
# def create_tables():
#     Base.metadata.create_all(bind=engine)

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(wallet_router, prefix="/wallets", tags=["wallets"])
app.include_router(pool_router, prefix="/pools", tags=["pools"])
