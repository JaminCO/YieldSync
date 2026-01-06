from fastapi import APIRouter, HTTPException, status, Depends
from app.models.schemas import UserSchema, WalletSchema, WalletBase, WalletCreate
from app.services.user_services import get_current_user_dep
from app.services.wallet_services import create_wallet, delete_wallet, get_wallet_balance_eth, get_balances
from typing import Dict, Any, List, Optional
from app.models.models import User, Wallet, Transaction, TokenTransfer, WalletActivityScore
from app.db import get_db
from sqlalchemy.orm import Session
from app.services.wallet_services import get_balances

router = APIRouter()

def orm_to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

@router.get("/me",description="Get my wallets", response_model=Dict[str, list[WalletSchema]])
async def get_my_wallet(current_user: User = Depends(get_current_user_dep)):
    wallets = current_user.wallets or []
    if wallets:
        wallet_dicts = [orm_to_dict(wallet) for wallet in wallets]
        for wallet in wallet_dicts:
            balance = get_wallet_balance_eth(wallet['address'])
            wallet['eth_balance'] = balance["eth"]
    return {"wallets": wallet_dicts}

@router.post("/me", description="Create a new wallet", response_model=WalletSchema)
async def create_my_wallet(wallet_data: WalletCreate, current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    wallet_data.user_id = current_user.id
    wallet = create_wallet(db, wallet_data)
    return wallet

@router.get("/analyze", description="Analyze my wallet")
async def analyze_my_wallet(current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    analysis_result = db.query(WalletActivityScore).filter(WalletActivityScore.wallet_address == wallet.address).first()
    if not analysis_result:
        raise HTTPException(status_code=404, detail="Wallet analysis not found")
    return analysis_result

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
    activity_score = db.query(WalletActivityScore).filter(WalletActivityScore.wallet_address == wallet.address).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    if wallet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this wallet")
    return {"wallet": wallet, "activity_analysis": activity_score}

@router.get("/{wallet_id}/balance", description="Get my wallet balance", response_model=Dict[str, Any])
def get_wallet_balance(wallet_id: int, current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    if wallet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this wallet")
    balance = get_balances(wallet.address)
    return {"address": wallet.address, "balance": balance}

@router.get("/transactions/{wallet_id}", description="Get wallet transactions", response_model=Dict[str, Any])
def get_wallet_transactions(wallet_id: int, current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    if wallet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this wallet")
    transactions = db.query(Transaction).filter(Transaction.wallet_id == wallet_id).all()
    transacts = [orm_to_dict(tx) for tx in transactions]
    return {"transactions": transacts}

@router.get("/token-transfers/{wallet_id}", description="Get wallet token transfers", response_model=Dict[str, Any])
def get_wallet_token_transfers(wallet_id: int, current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    if wallet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this wallet")
    token_transfers = db.query(TokenTransfer).filter(TokenTransfer.wallet_id == wallet_id).all()
    transacts = [orm_to_dict(tx) for tx in token_transfers]
    return {"token_transfers": transacts}