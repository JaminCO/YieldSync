import json
import datetime
from typing import Dict, Any, List, Optional
import requests
import math
from app.pull_data import fetch_pools, fetch_protocol_details, apy_search

def score_defillama_pool(pool: dict) -> dict:
    """
    Takes a DefiLlama pool object and returns:
    - apy
    - tvl_score (0-100)
    - risk_score (0-100)
    - final_score (0-100)
    - pool (the original pool data)
    """
    # 1) APY
    apy = pool.get("apy")
    if pool.get("apyBase") or pool.get("apyReward"):
        apy = (pool.get("apyBase") or 0) + (pool.get("apyReward") or 0)

    # 2) TVL score (log-scaled, 0-100)
    tvl_usd = pool.get("tvlUsd") or 0
    tvl_score = min(100, round(math.log10(tvl_usd + 1) * 20, 2))

    # 3) Risk factors
    il_risk = pool.get("ilRisk", "no")
    stablecoin = pool.get("stablecoin", False)
    predicted_prob = (pool.get("predictions") or {}).get("predictedProbability", 100)
    sigma = pool.get("sigma", 0)
    exposure = pool.get("exposure", "single")

    # Normalize
    tvl_norm = 1 - min(tvl_usd / 40_000_000_000, 1)   # larger TVL = lower risk
    apy_norm = min(apy / 500, 1)                      # very high APY = higher risk
    volatility_norm = min(sigma / 1.0, 1)             # cap sigma at ~1.0
    il_penalty = 0.2 if str(il_risk).lower() == "yes" else 0
    stablecoin_penalty = 0.1 if not stablecoin else 0
    prediction_penalty = 1 - (predicted_prob / 100) if predicted_prob else 1
    exposure_penalty = 0.05 if str(exposure).lower() == "multi" else 0

    # Weighted risk (0-1)
    risk_score = (
        0.3 * tvl_norm +
        0.2 * apy_norm +
        0.2 * volatility_norm +
        0.1 * prediction_penalty +
        il_penalty +
        stablecoin_penalty +
        exposure_penalty
    )
    risk_score = min(risk_score, 1.0)
    risk_score_percent = round(risk_score * 100, 2)

    # 4) Final score
    final_score = round((apy * 0.5) + (tvl_score * 0.3) - (risk_score_percent * 0.2), 2)

    # final_score = max(0, min(final_score, 100))  # clamp to 0–100

    # Explanations
    reasons = []
    if apy > 50: reasons.append("Very high APY may be unsustainable.")
    if tvl_usd < 100_000_000: reasons.append("Low TVL increases volatility risk.")
    if il_risk.lower() == "yes": reasons.append("Impermanent loss risk present.")
    if not stablecoin: reasons.append("Non-stablecoin pool, subject to volatility.")
    if exposure != "single": reasons.append("Multi-token exposure increases complexity.")
    if not reasons: reasons.append("Pool appears relatively safe.")

    return {
        "apy": round(apy, 4),
        "tvl_score": tvl_score,
        "risk_score": f"{risk_score_percent}%",
        "final_score": final_score,
        "breakdown": {
            "tvl": f"Liquidity: ${tvl_usd:,.0f} → score {tvl_score}",
            "impermanent_loss": "Yes" if il_risk == "yes" else "No",
            "stablecoin": "Stablecoin pool" if stablecoin else "Volatile tokens",
            "volatility_sigma": f"{sigma:.3f} (normalized {volatility_norm:.2f})",
            "prediction_confidence": f"{predicted_prob}%",
            "exposure": "Multi-asset" if exposure == "multi" else "Single-asset",
            "explanation": " ".join(reasons)
        },
        "pool": pool  # Add the original pool data to the response
    }

def get_top_pools(pools: List[dict], top_n: int = 5) -> List[dict]:
    scored_pools = [score_defillama_pool(pool) for pool in pools]
    sorted_pools = sorted(scored_pools, key=lambda x: x["final_score"], reverse=True)
    return sorted_pools[:top_n]