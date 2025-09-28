from celery import Celery
from app.core.config import settings
from app.pull_data import fetch_pools, fetch_protocol_details
from app.models.models import Recommendation, Protocol, Pool, User, Wallet, Transaction, TokenTransfer, WalletActivityScore,
from app.db import get_db
from app.services.rec_engine import score_defillama_pool
from sqlalchemy.orm import Session
import json
import requests

celery_app = Celery(
    "yieldsync_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)
@celery_app.task
def pull_wallet_information():
    return "Celery is working!"

@celery_app.task
def pull_protocol_data(slug: str):
    db: Session = next(get_db())
    protocols = fetch_protocol_details(slug)
    if not protocols:
        return None
        
    proto_json = protocols
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
    slug=proto_json.get("slug"),
    )

    db.add(protocol)
    db.commit()
    db.refresh(protocol)

    return protocols

@celery_app.task
def pull_pool_data(limit: int = 10):
    db: Session = next(get_db())
    pools = fetch_pools(limit)
    if not pools:
        return None

    for pool_json in pools:
        score = score_defillama_pool(pool_json)
        protocol = db.query(Protocol).filter(Protocol.name == pool_json.get("project")).first()
        if not protocol:
            pull_protocol_data.delay(pool_json.get("project"))
            continue

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
        )

        db.add(pool)


    db.commit()
    db.refresh(pool)
    return score


@celery_app.task
def ai_personalised_recommendations(pool_id: int, user_id: str):
    db: Session = next(get_db())
    pool = db.query(Pool).filter(Pool.id == pool_id).first()
    user = db.query(User).filter(User.id == user_id).first()
    if not pool:
        return None

    # Placeholder for AI recommendation logic
    

    return recommendation