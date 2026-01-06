from celery import Celery
from app.core.config import settings
from app.services.pull_data import fetch_pools, fetch_protocol_details
from app.models.models import Recommendation, Protocol, Pool, User, Wallet, Transaction, TokenTransfer, WalletActivityScore
from app.db import get_db
from app.services.rec_engine import score_defillama_pool
from app.services.utils import ExplanationEngine, PersonalizationEngine, WalletAnalyzer
from app.services.wallet_services import get_balances
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import json
import requests
import time
import os
from datetime import datetime



load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
BASE_URL = os.getenv("ETHERSCAN_BASE_URL")

limit = 50


def pull_wallet_transactions(address: str, chain: str = "ETH"):
    db: Session = next(get_db())
    wallet_id = db.query(Wallet).filter(Wallet.address == address).first().id

    transaction_list = []
    internal_transaction_list = []
    token_transfer_list = []

    def get(endpoint, params):
        params.update({"chainid":1, "module": "account", "address": address, "apikey": ETHERSCAN_API_KEY})
        # "offset": limit, "page": 1
        response = requests.get(BASE_URL, params=params)
        return response.json().get("result", [])

    # Fetch normal transactions
    normal_txs = get("txlist", {"action": "txlist", "startblock": 0, "endblock": 99999999, "sort": "desc"})
    for tx in normal_txs[:limit]:
        existing_hashes = {t[0] for t in db.query(Transaction.tx_hash).filter(Transaction.wallet_id == wallet_id).all()}
        if tx["hash"] in existing_hashes:
            continue
        transaction_list.append(Transaction(
            wallet_id=wallet_id,
            chain=chain,
            tx_hash=tx["hash"],
            tx_type="normal",
            from_address=tx["from"],
            to_address=tx.get("to"),
            value=float(tx["value"]) / float(1e18),
            gas_used=int(tx["gasUsed"]),
            gas_price=float(tx["gasPrice"]) / float(1e9),
            timestamp=str(datetime.fromtimestamp(int(tx["timeStamp"]))),
            input_data=tx.get("input"),
            is_error=tx["isError"] == "1",
            internal_tx_count=0,
            status="success" if tx.get("txreceipt_status") == "1" else "failure"
        ))



    # Fetch internal transactions
    internal_txs = get("txlistinternal", {"action": "txlistinternal", "startblock": 0, "endblock": 99999999, "sort": "desc"})
    internal_count = {}
    for tx in internal_txs[:limit]:
        tx_hash = tx["hash"]
        internal_count[tx_hash] = internal_count.get(tx_hash, 0) + 1
        internal_transaction_list.append(Transaction(
            wallet_id=wallet_id,
            chain=chain,
            tx_hash=tx_hash,
            tx_type="internal",
            from_address=tx["from"],
            to_address=tx.get("to"),
            value=float(tx["value"]) / float(1e18),
            gas_used=int(tx["gasUsed"]),
            gas_price=float(tx["gas"]) / float(1e9),  # fallback if gasPrice missing
            timestamp=str(datetime.fromtimestamp(int(tx["timeStamp"]))),
            input_data=None,
            is_error=tx["isError"] == "1",
            internal_tx_count=internal_count[tx_hash],
            status="success" if tx.get("isError") == "0" else "failure"
        ))

    # Fetch token transfers
    token_txs = get("tokentx", {"action": "tokentx", "startblock": 0, "endblock": 99999999, "sort": "desc"})
    for tx in token_txs[:limit]:
        token_amount = float(tx["value"]) / float(10 ** int(tx["tokenDecimal"]))
        token_transfer_list.append(TokenTransfer(
            wallet_id=wallet_id,
            chain=chain,
            tx_hash=tx["hash"],
            token_decimal=tx["tokenDecimal"],
            token_name=tx["tokenName"],
            token_address=tx["contractAddress"],
            token_symbol=tx["tokenSymbol"],
            from_address=tx["from"],
            to_address=tx.get("to"),
            token_amount=token_amount,
            token_type="ERC20",  # You can add logic to detect ERC721 if needed
            timestamp=str(datetime.fromtimestamp(int(tx["timeStamp"])))
        ))
        # Save transactions safely in order
    try:
        if transaction_list:
            db.bulk_save_objects(transaction_list)
        if internal_transaction_list:
            db.bulk_save_objects(internal_transaction_list)
        db.commit()  # Ensure tx_hash rows exist before token transfers

        if token_transfer_list:
            db.bulk_save_objects(token_transfer_list)
            db.commit()
    except Exception as e:
        db.rollback()
        raise e


    return {
        "transaction_list": transaction_list,
        "internal_transaction_list": internal_transaction_list,
        "token_transfer_list": token_transfer_list
    }

def analyze_wallet_data(address):

    db: Session = next(get_db())
    wallet = db.query(Wallet).filter(Wallet.address == address).first()
    wallet_id = wallet.id if wallet else None

    if not wallet:
        return None
    if db.query(WalletActivityScore).filter(WalletActivityScore.wallet_address == wallet.address).first():
        return None  # Skip if analysis already exists
    analyzer = WalletAnalyzer()
    wallet_data = {
        "transaction_list": [tx.__dict__ for tx in db.query(Transaction).filter(Transaction.wallet_id == wallet_id).all()],
        "token_transfer_list": [tt.__dict__ for tt in db.query(TokenTransfer).filter(TokenTransfer.wallet_id == wallet_id).all()],
        "balance": get_balances(wallet.address)
    }

    analysis_result = analyzer.analyze_wallet(wallet_data)

    if analysis_result:
        score_entry = WalletActivityScore(
            wallet_address=wallet.address,
            score=analysis_result.get("score"),
            last_active=analysis_result.get("last_active"),
            ai_recommendation=analysis_result.get("ai_recommendation"),
            top_tokens=analysis_result.get("top_tokens"),
            risk_profile=analysis_result.get("risk_profile"),
            common_token_types=analysis_result.get("common_token_types"),
            portfolio_summary=analysis_result.get("portfolio_summary")
        )
        db.add(score_entry)
        db.commit()
        db.refresh(score_entry)
        return score_entry
    return None

def pull_protocol_data(slug: str):
    db: Session = next(get_db())
    protocols = fetch_protocol_details(slug)
    prots = None
    if not protocols:
        return None
        
    proto_json = protocols
    existing_protocol = db.query(Protocol).filter(Protocol.protocol_id == proto_json.get("id")).first()

    if existing_protocol:
        # Update existing protocol
        existing_protocol.name = proto_json.get("name")
        existing_protocol.address = proto_json.get("address")
        existing_protocol.symbol = proto_json.get("symbol")
        existing_protocol.url = proto_json.get("url")
        existing_protocol.description = proto_json.get("description")
        existing_protocol.chain = proto_json.get("chain")
        existing_protocol.logo = proto_json.get("logo")
        existing_protocol.audits = proto_json.get("audits")
        existing_protocol.category = proto_json.get("category")
        existing_protocol.twitter = proto_json.get("twitter")
        existing_protocol.parent_protocol = proto_json.get("parentProtocol")
        existing_protocol.chains = proto_json.get("chains")
        existing_protocol.chain_tvls = proto_json.get("chainTvls")
        existing_protocol.listed_at = proto_json.get("listedAt")
        existing_protocol.slug = proto_json.get("slug") or proto_json.get("name").lower().replace(" ", "-")
        
        db.commit()
        db.refresh(existing_protocol)
        prots = existing_protocol
    else:
        # Insert new protocol
        protocol = Protocol(
            name=proto_json.get("name"),
            protocol_id=proto_json.get("id"),
            address=proto_json.get("address"),
            symbol=proto_json.get("symbol"),
            url=proto_json.get("url"),
            description=proto_json.get("description"),
            chain=proto_json.get("chain"),
            logo=proto_json.get("logo"),
            audits=proto_json.get("audits"),
            category=proto_json.get("category"),
            twitter=proto_json.get("twitter"),
            parent_protocol=proto_json.get("parentProtocol"),
            chains=proto_json.get("chains"),
            chain_tvls=proto_json.get("chainTvls"),
            listed_at=proto_json.get("listedAt"),
            slug=proto_json.get("slug") or proto_json.get("name").lower().replace(" ", "-")
        )

        db.add(protocol)
        db.commit()
        db.refresh(protocol)
        prots = protocol

    return prots

def pull_pool_data(limit: int = 10):
    db: Session = next(get_db())
    pools = fetch_pools(limit)
    print(f"Fetched {len(pools)} pools from external API.")
    if not pools:
        return None

    explanation_engine = ExplanationEngine()
    created_pools = []  # List to keep track of created pools

    for pool_json in pools:
        score = score_defillama_pool(pool_json)
        print(f"Project: {pool_json.get('project')}")
        protocol = db.query(Protocol).filter(Protocol.name == pool_json.get("project").title()).first()
        print(f"Processing pool: {pool_json.get('pool')} with protocol: {pool_json.get('project')}")
        print(f"Found protocol: {protocol}")
        if not protocol:
            protocol = pull_protocol_data(pool_json.get("project"))
            continue


        if db.query(Pool).filter(Pool.pool_id == pool_json.get("pool")).first():
            print(f"Pool {pool_json.get('pool')} already exists. Skipping.")
            continue  # Skip existing pools
        explanation = explanation_engine.generate_explanation(pool_json, score)
        time.sleep(60)  # To avoid hitting rate limits
        action = explanation_engine.generate_action(pool_json, score)

        pool = Pool(
            pool_id=pool_json.get("pool"),
            protocol_id=protocol.id,
            pool_name=f"{pool_json.get('project')} - {pool_json.get('symbol')}",
            chain=pool_json.get("chain"),
            project=pool_json.get("project"),
            symbol=pool_json.get("symbol"),
            tvl_usd=pool_json.get("tvlUsd"),
            apy_base=pool_json.get("apyBase"),
            apy_reward=pool_json.get("apyReward"),
            apy=pool_json.get("apy"),
            predictions=pool_json.get("predictions"),
            pool_meta=pool_json.get("poolMeta"),
            stablecoin=pool_json.get("stablecoin"),
            il_risk=pool_json.get("ilRisk"),
            exposure=pool_json.get("exposure"),
            reward_tokens=pool_json.get("rewardTokens"),
            underlying_tokens=pool_json.get("underlyingTokens"),
            volume_usd_1d=pool_json.get("volumeUsd1d"),
            volume_usd_7d=pool_json.get("volumeUsd7d"),
            mu=pool_json.get("mu"),
            sigma=pool_json.get("sigma"),
            count=pool_json.get("count"),
            outlier=pool_json.get("outlier"),
            tvl_score=score.get("tvl_score"),
            risk_score=score.get("risk_score"),
            final_score=score.get("final_score"),
            breakdown=score.get("breakdown"),
            summary=explanation,
            action=action,
        )

        db.add(pool)
        created_pools.append(pool)
        print(f"Added pool: {pool.pool_name}")

    print(f"Pulled {len(created_pools)} new pools.")
    db.commit()

    # Refresh all created pools
    for pool in created_pools:
        db.refresh(pool)

    return score

def ai_personalised_recommendations(pool_id: int, user_id: str):
    db: Session = next(get_db())
    pool = db.query(Pool).filter(Pool.id == pool_id).first()
    user = db.query(User).filter(User.id == user_id).first()
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    wallet_analysis = None
    if wallet:
        wallet_analysis = db.query(WalletActivityScore).filter(WalletActivityScore.wallet_address == wallet.address).first()

    if not pool:
        return None

    # build profiles defensively
    user_profile = {}
    wallet_profile = {}
    pool_data = {}

    if user:
        try:
            user_profile = {c.name: getattr(user, c.name) for c in user.__table__.columns}
            if wallet:
                user_profile["balance"] = get_balances(wallet.address)
        except Exception:
            user_profile = {k: v for k, v in vars(user).items() if not k.startswith('_')}

    if wallet_analysis:
        try:
            wallet_profile = {c.name: getattr(wallet_analysis, c.name) for c in wallet_analysis.__table__.columns}
        except Exception:
            wallet_profile = {k: v for k, v in vars(wallet_analysis).items() if not k.startswith('_')}

    try:
        pool_data = {c.name: getattr(pool, c.name) for c in pool.__table__.columns}
    except Exception:
        pool_data = {k: v for k, v in vars(pool).items() if not k.startswith('_')}

    # call personalization engine (match signature)
    personalization = PersonalizationEngine()
    personal_exp = personalization.generate_explanation(user_profile=user_profile, score_result=wallet_profile, pool_data=pool_data)
    personal_action = personalization.generate_action(user_profile=user_profile, score_result=wallet_profile, pool_data=pool_data)

    recommendation = Recommendation(
        user_id=user_id,
        pool_id=pool_id,
        protocol_id=pool.protocol_id,
        score=pool.final_score,
        apy=pool.apy,
        tvl_score=pool.tvl_score,
        risk_score=pool.risk_score,
        projected_roi=None,
        details=personal_exp,
        next_steps=personal_action,
        breakdown=pool.breakdown,
    )

    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)

    return recommendation

def start_test(user_id: str):
    db: Session = next(get_db())
    score = pull_pool_data(limit=1)
    print("Pulled pool data with score:", score)
    tx_list = pull_wallet_transactions("0x2908537D5e56F5BCEf80A1Fd7E8Ad3E05971C99E")
    print(f"Pulled {len(tx_list['transaction_list'])} transactions.")
    score_entry = analyze_wallet_data("0x2908537D5e56F5BCEf80A1Fd7E8Ad3E05971C99E")
    if score_entry:
        print("Wallet analysis score:", score_entry)
    else:
        print("No new wallet analysis created.")
    for pool in db.query(Pool).limit(1).all():
        rec = ai_personalised_recommendations(pool.id, user_id)
    return {"status": "Test completed", "pool_score": score, "transactions_pulled": len(tx_list['transaction_list']), "wallet_analysis_score": score_entry.score if score_entry else None, "recommendation_id": rec.id if rec else None}

