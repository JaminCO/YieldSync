# app/db/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, Enum, Boolean, TIMESTAMP, Text, JSON
from sqlalchemy.orm import relationship
from app.db import Base, engine

from datetime import datetime

from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship, declarative_base
import uuid


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=False, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    primary_goal = Column(String, default="earn steady, low-risk yield")
    risk_tolerance = Column(String, default="low")
    experience_level = Column(String, default="beginner")

    wallets = relationship("Wallet", back_populates="user")
    
class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    address = Column(String, unique=True, index=True, nullable=False)
    chain = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    transactions = relationship("Transaction", back_populates="wallet")
    activity_score = relationship("WalletActivityScore", back_populates="wallet")
    user = relationship("User", back_populates="wallets")

class Transaction(Base):
    """
    Represents both normal and internal Ethereum transactions.
    
    Fields:
        tx_hash (str): Unique transaction hash (primary key).
        tx_type (str): 'normal' or 'internal' to distinguish transaction type.
        from_address (str): Sender's wallet address.
        to_address (str): Receiver's wallet address.
        value (Decimal): Amount of ETH transferred (0 for internal if not ETH).
        gas_used (int): Gas used for the transaction.
        gas_price (Decimal): Gas price paid.
        block_number (int): Block number in which the transaction was included.
        timestamp (datetime): When the transaction was mined.
        input_data (str): Encoded input for smart contract call.
        is_error (bool): Whether the transaction failed.
        internal_tx_count (int): Number of internal transactions triggered.
        status (str): Status from receipt (e.g., 'success', 'failure').

    Purpose:
        Stores all on-chain transaction data (normal and internal) for each wallet,
        enabling analytics on ETH spending, DeFi interactions, and contract activity.
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"))
    chain = Column(String, index=True, nullable=False)
    tx_hash = Column(String, unique=True, nullable=False)
    tx_type = Column(Enum('normal', 'internal', name='tx_type'), nullable=False)
    from_address = Column(String, nullable=False)
    to_address = Column(String, nullable=True)
    value = Column(Numeric, nullable=False)
    gas_used = Column(Integer, nullable=False)
    gas_price = Column(Numeric, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    input_data = Column(String, nullable=True)
    is_error = Column(Boolean, nullable=False)
    internal_tx_count = Column(Integer, nullable=False)
    status = Column(String, nullable=False)

    wallet = relationship("Wallet", back_populates="transactions")
    token_transfers = relationship("TokenTransfer", back_populates="transaction")


class TokenTransfer(Base):
    """
    Represents an ERC-20 or ERC-721 token transfer event.

    Fields:
        tx_hash (str): Transaction hash, links to the transactions table.
        token_address (str): Smart contract address of the token.
        token_symbol (str): Symbol of the token (e.g., USDT, DAI).
        from_address (str): Sender's wallet address.
        to_address (str): Receiver's wallet address.
        token_amount (Decimal): Amount of token transferred.
        token_type (str): Type of token, either 'ERC20' or 'ERC721'.
        timestamp (datetime): When the token transfer occurred.

    Purpose:
        Stores all token transfer events for wallets, enabling portfolio tracking,
        token analytics, and behavioral insights.
    """
    
    __tablename__ = "token_transfers"

    tx_hash = Column(String, ForeignKey("transactions.tx_hash"), primary_key=True)
    token_address = Column(String, nullable=False)
    token_symbol = Column(String, nullable=False)
    from_address = Column(String, nullable=False)
    to_address = Column(String, nullable=True)
    token_amount = Column(Numeric, nullable=False)
    token_type = Column(Enum("ERC20", "ERC721", name="token_type"), nullable=False)
    timestamp = Column(DateTime, nullable=False)

    transaction = relationship("Transaction", back_populates="token_transfers")

class WalletActivityScore(Base):
    """
    Represents a wallets's activity score and AI-driven analysis for an Ethereum wallet.
    Attributes:
        user_address (str): The Ethereum address of the user (primary key, foreign key to wallets.address).
        score (Decimal): Personalized activity score (e.g., 0.00–99.99), calculated from transaction behavior.
        last_active (datetime): Timestamp of the user's most recent recorded activity.
        ai_recommendation (str, optional): AI-generated recommendation based on the user's transaction and token activity.
        top_tokens (str, optional): JSON-encoded list of the user's most interacted tokens.
        risk_profile (str, optional): AI-generated risk category for the user (e.g., 'low', 'medium', 'high').
    Table:
        Wallet_activity_score
    Purpose:
        Stores analytics and AI insights for each wallet, enabling personalized recommendations,
        risk assessment, and behavioral analysis based on on-chain activity.
    """

    __tablename__ = "Wallet_activity_score"

    wallet_address = Column(String, ForeignKey("wallets.address"), primary_key=True)
    score = Column(Integer, nullable=False)
    last_active = Column(DateTime, nullable=False)
    ai_recommendation = Column(String, nullable=True)
    top_tokens = Column(String, nullable=True)
    risk_profile = Column(String, nullable=True)
    common_token_types = Column(String, nullable=True)
    portfolio_summary = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    wallet = relationship("Wallet", back_populates="activity_score")

# -------------------------------
# Protocols Table
# -------------------------------
class Protocol(Base):
    __tablename__ = "protocols"

    id = Column(Integer, primary_key=True, index=True)
    protocol_id = Column(Integer, unique=True, nullable=True)  # from DefiLlama API
    slug = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=True)
    symbol = Column(String(50), nullable=True)
    url = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    chain = Column(String(100), nullable=True)
    logo = Column(String(255), nullable=True)
    audits = Column(String(50), nullable=True)
    category = Column(String(100), nullable=True)
    twitter = Column(String(100), nullable=True)
    parent_protocol = Column(String(255), nullable=True)
    chains = Column(JSONB, nullable=True)             # list of supported chains
    chain_tvls = Column(JSONB, nullable=True)         # TVL time series
    listed_at = Column(Integer, nullable=True)        # timestamp from API

    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    pools = relationship("Pool", back_populates="protocol")
    recommendations = relationship("Recommendation", back_populates="protocol")


# -------------------------------
# Pools Table
# -------------------------------
class Pool(Base):
    __tablename__ = "pools"

    id = Column(Integer, primary_key=True, index=True)
    protocol_id = Column(Integer, ForeignKey("protocols.id", ondelete="CASCADE"))
    pool_id = Column(UUID(as_uuid=True), nullable=False, unique=True) # from DefiLlama UUID
    pool_name = Column(String(255), nullable=True)

    chain = Column(String(100), nullable=True)
    project = Column(String(255), nullable=True)
    symbol = Column(String(50), nullable=True)

    # Metrics
    tvl_usd = Column(Numeric, nullable=True)
    apy_base = Column(Numeric, nullable=True)
    apy_reward = Column(Numeric, nullable=True)
    apy = Column(Numeric, nullable=True)
    apy_pct_1d = Column(Numeric, nullable=True)
    apy_pct_7d = Column(Numeric, nullable=True)
    apy_pct_30d = Column(Numeric, nullable=True)
    apy_mean_30d = Column(Numeric, nullable=True)
    apy_base_inception = Column(Numeric, nullable=True)

    # Other Data
    predictions = Column(JSONB, nullable=True)  # Store prediction data from DefiLlama
    pool_meta = Column(String, nullable=True)  # Store additional metadata from DefiLlama

    # Risk & AI enrichment
    stablecoin = Column(Boolean, default=False)
    il_risk = Column(String(50), nullable=True)
    exposure = Column(String(100), nullable=True)
    
    risk_score = Column(Numeric, nullable=True)
    summary = Column(Text, nullable=True)
    action = Column(Text, nullable=True)
    final_score = Column(Numeric, nullable=True)
    breakdown = Column(JSONB, nullable=True)  # Store explanation, breakdown, etc.

    metadata = Column(JSONB, nullable=True)
    supported_chains = Column(JSONB, nullable=True)
    underlying_assets = Column(JSONB, nullable=True)

    # Rewards/tokens
    reward_tokens = Column(JSONB, nullable=True)
    underlying_tokens = Column(JSONB, nullable=True)

    # Volumes/volatility
    volume_usd_1d = Column(Numeric, nullable=True)
    volume_usd_7d = Column(Numeric, nullable=True)
    mu = Column(Numeric, nullable=True)
    sigma = Column(Numeric, nullable=True)
    count = Column(Integer, nullable=True)
    outlier = Column(Boolean, default=False)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    protocol = relationship("Protocol", back_populates="pools")
    recommendations = relationship("Recommendation", back_populates="pool")


# -------------------------------
# Recommendations Table
# -------------------------------
class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)  # connect to users table later
    pool_id = Column(Integer, ForeignKey("pools.id", ondelete="CASCADE"))
    protocol_id = Column(Integer, ForeignKey("protocols.id", ondelete="CASCADE"))

    # Scores & projections
    score = Column(Numeric, nullable=True)
    apy = Column(Numeric, nullable=True)
    tvl_score = Column(Numeric, nullable=True)
    risk_score = Column(Numeric, nullable=True)
    projected_roi = Column(Numeric, nullable=True)
    final_score = Column(Numeric, nullable=True)

    # AI explanation
    details = Column(Text, nullable=True)
    risks = Column(Text, nullable=True)
    next_steps = Column(Text, nullable=True)
    breakdown = Column(JSONB, nullable=True)  # Store explanation, breakdown, etc.

    # Risk metadata JSON (AI generated)
    risk_metadata = Column(JSONB, nullable=True)
    # Example:
    # {
    #   "overall_risk_score": 72,
    #   "liquidity_risk": "moderate",
    #   "smart_contract_risk": "low",
    #   "market_risk": "high",
    #   "operational_risk": "moderate"
    # }

    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    pool = relationship("Pool", back_populates="recommendations")
    protocol = relationship("Protocol", back_populates="recommendations")

Base.metadata.create_all(bind=engine)