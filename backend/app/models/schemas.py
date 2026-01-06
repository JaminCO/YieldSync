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
    common_token_types: Optional[str]
    portfolio_summary: Optional[str]

class WalletActivityScoreCreate(WalletActivityScoreBase):
    pass

class WalletActivityScoreSchema(WalletActivityScoreBase):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# Login Request Schema
class LoginRequest(BaseModel):
    email: str
    password: str

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal

# -------------------------------
# Protocol Schemas
# -------------------------------
class ProtocolBase(BaseModel):
    name: str
    address: Optional[str] = None
    symbol: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    chain: Optional[str] = None
    logo: Optional[str] = None
    audits: Optional[str] = None
    category: Optional[str] = None
    twitter: Optional[str] = None
    parent_protocol: Optional[str] = None
    chains: Optional[List[str]] = None
    chain_tvls: Optional[Dict[str, Decimal]] = None
    listed_at: Optional[int] = None

class ProtocolCreate(ProtocolBase):
    pass

class ProtocolSchema(ProtocolBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# -------------------------------
# Pool Schemas
# -------------------------------
class PoolBase(BaseModel):
    protocol_id: int
    pool_uid: Optional[str] = None
    pool_name: Optional[str] = None
    chain: Optional[str] = None
    project: Optional[str] = None
    symbol: Optional[str] = None
    tvl_usd: Optional[Decimal] = None
    apy_base: Optional[Decimal] = None
    apy_reward: Optional[Decimal] = None
    apy: Optional[Decimal] = None
    apy_pct_1d: Optional[Decimal] = None
    apy_pct_7d: Optional[Decimal] = None
    apy_pct_30d: Optional[Decimal] = None
    apy_mean_30d: Optional[Decimal] = None
    apy_base_inception: Optional[Decimal] = None
    stablecoin: Optional[bool] = None
    il_risk: Optional[str] = None
    exposure: Optional[str] = None
    risk_score: Optional[Decimal] = None
    summary: Optional[str] = None
    action: Optional[str] = None
    final_score: Optional[Decimal] = None
    other_data: Optional[Dict[str, Any]] = None
    supported_chains: Optional[List[str]] = None
    underlying_assets: Optional[List[str]] = None
    reward_tokens: Optional[List[str]] = None
    underlying_tokens: Optional[List[str]] = None
    volume_usd_1d: Optional[Decimal] = None
    volume_usd_7d: Optional[Decimal] = None
    mu: Optional[Decimal] = None
    sigma: Optional[Decimal] = None
    count: Optional[int] = None
    outlier: Optional[bool] = None

class PoolCreate(PoolBase):
    pass

class PoolSchema(PoolBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# -------------------------------
# Recommendation Schemas
# -------------------------------
class RecommendationBase(BaseModel):
    user_id: Optional[int] = None
    pool_id: int
    protocol_id: int
    score: Optional[Decimal] = None
    apy: Optional[Decimal] = None
    tvl_score: Optional[Decimal] = None
    risk_score: Optional[Decimal] = None
    projected_roi: Optional[Decimal] = None
    final_score: Optional[Decimal] = None
    details: Optional[str] = None
    risks: Optional[str] = None
    next_steps: Optional[str] = None
    rationale: Optional[str] = None
    risk_metadata: Optional[Dict[str, Any]] = None

class RecommendationCreate(RecommendationBase):
    pass

class RecommendationSchema(RecommendationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True