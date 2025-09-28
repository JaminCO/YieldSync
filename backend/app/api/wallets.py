from fastapi import APIRouter, HTTPException, status, Depends
from app.models.schemas import UserSchema, WalletSchema, WalletBase, WalletCreate
from app.services.user_services import get_current_user_dep
from app.services.wallet_services import create_wallet, delete_wallet, get_wallet_balance_eth
from typing import Dict, Any, List, Optional
from app.models.models import User, Wallet
from app.db import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/me",description="Get my wallets", response_model=Dict[str, Any])
async def get_my_wallet(current_user: User = Depends(get_current_user_dep)):
    wallets = current_user.wallets
    if not wallets:
        wallets = []
    return {"wallets": wallets}

@router.post("/me", description="Create a new wallet", response_model=WalletSchema)
async def create_my_wallet(wallet_data: WalletCreate, current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    wallet_data.user_id = current_user.id
    wallet = create_wallet(db, wallet_data)
    return wallet

@router.delete("/{wallet_id}", description="Delete my wallet")
async def delete_my_wallet(wallet_id: int, current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    if wallet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this wallet")
    wallet = delete_wallet(db, wallet)
    return wallet

@router.get("/{wallet_id}", description="Get my wallet", response_model=WalletSchema)
def get_wallet(wallet_id: int, current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    if wallet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this wallet")
    return wallet

@router.get("/{wallet_id}/balance", description="Get my wallet balance", response_model=Dict[str, Any])
def get_wallet_balance(wallet_id: int, current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    if wallet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this wallet")
    balance = get_wallet_balance_eth(wallet.address)
    return {"address": wallet.address, "balance": balance}