from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

# User Schemas
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserSchema(UserBase):
    id: int

    class Config:
        from_attributes = True

# Wallet Schemas
class WalletBase(BaseModel):
    address: str
    chain: str

class WalletCreate(WalletBase):
    user_id: int | None = None

class WalletSchema(WalletBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Transaction Schemas
class TransactionBase(BaseModel):
    wallet_id: int
    chain: str
    tx_hash: str
    tx_type: str
    from_address: str
    to_address: Optional[str]
    value: Decimal
    gas_used: int
    gas_price: Decimal
    timestamp: datetime
    input_data: str
    is_error: bool
    internal_tx_count: int
    status: str

class TransactionCreate(TransactionBase):
    pass

class TransactionSchema(TransactionBase):
    id: int

    class Config:
        from_attributes = True

# TokenTransfer Schemas
class TokenTransferBase(BaseModel):
    tx_hash: str
    token_address: str
    token_symbol: str
    from_address: str
    to_address: Optional[str]
    token_amount: Decimal
    token_type: str
    timestamp: datetime

class TokenTransferCreate(TokenTransferBase):
    pass

class TokenTransferSchema(TokenTransferBase):
    class Config:
        from_attributes = True

# WalletActivityScore Schemas
class WalletActivityScoreBase(BaseModel):
    wallet_address: str
    score: int
    last_active: datetime
    ai_recommendation: Optional[str]
    top_tokens: Optional[str]
    risk_profile: Optional[str]

class WalletActivityScoreCreate(WalletActivityScoreBase):
    pass

class WalletActivityScoreSchema(WalletActivityScoreBase):
    class Config:
        from_attributes = True

# Login Request Schema
class LoginRequest(BaseModel):
    email: str
    password: str

