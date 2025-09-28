from fastapi import APIRouter, HTTPException, status, Depends
from app.models.models import User, Wallet, Transaction, TokenTransfer, WalletActivityScore, Pool, Protocol, Recommendation
from app.db import SessionLocal
from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import Query

router = APIRouter()

def get_db():
    try:
        # Create a new session
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    except Exception as e:
        print(f"DATABASE_CONNECTION_ERROR {e}")
        raise e

@router.get("/pools", description="Fetch pools with optional filters")
async def get_pools_endpoint(
    db: Session = Depends(get_db),
    protocol: Optional[str] = Query(None, description="Filter by protocol name"),
    chain: Optional[str] = Query(None, description="Filter by chain"),
    min_risk_score: Optional[float] = Query(None, description="Minimum risk score"),
    max_risk_score: Optional[float] = Query(None, description="Maximum risk score"),
    min_apy: Optional[float] = Query(None, description="Minimum APY"),
    max_apy: Optional[float] = Query(None, description="Maximum APY"),
    sort_by: Optional[str] = Query("apy", description="Sort by 'apy' or 'risk_score'"),
    order: Optional[str] = Query("desc", description="Order: 'asc' or 'desc'")
):
    query = db.query(Pool)

    if protocol:
        query = query.filter(Pool.project == protocol)
    if chain:
        query = query.filter(Pool.chain == chain)
    if min_risk_score is not None:
        query = query.filter(Pool.risk_score >= min_risk_score)
    if max_risk_score is not None:
        query = query.filter(Pool.risk_score <= max_risk_score)
    if min_apy is not None:
        query = query.filter(Pool.apy >= min_apy)
    if max_apy is not None:
        query = query.filter(Pool.apy <= max_apy)

    if sort_by not in {"apy", "risk_score"}:
        sort_by = "apy"
    sort_column = getattr(Pool, sort_by)

    if order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    pools = query.all()
    return {"pools": pools}



@router.get("/protocols", description="Fetch protocols from external API")
async def get_protocols_endpoint(db: Session = Depends(get_db)):
    protocols = db.query(Protocol).all()
    return {"protocols": protocols}

@router.get("/recommendations/{user_id}", description="Get pool recommendations for a user")
async def get_recommendations_endpoint(user_id: str, db: Session = Depends(get_db)):
    recommendations = db.query(Recommendation).filter(Recommendation.user_id == user_id).all()
    return {"user_id": user_id, "recommendations": recommendations}

@router.get("/recommendations/{id}", description="Get Specific Recommendation by ID")
async def get_specific_recommendation_endpoint(id: str, db: Session = Depends(get_db)):
    recommendation = db.query(Recommendation).filter(Recommendation.id == id).first()
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return {"id": id, "recommendation": recommendation}