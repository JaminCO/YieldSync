import os
import json
from typing import Dict, Any, Optional
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    """Client for interacting with Google Gemini API"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        
    def generate_structured_response(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """
        Generate structured response from Gemini with error handling
        """
        try:
            # Combine system and user prompts
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            # Generate content
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    max_output_tokens=2048,
                )
            )
            
            # Extract text and parse JSON
            response_text = response.text.strip()
            
            return response_text

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response from Gemini: {e}")
        except Exception as e:
            raise

# Singleton instance
gemini_client = GeminiClient()

class ExplanationEngine:
    """Generates human-readable explanations for pool recommendations"""
    
    def __init__(self):
        self.explanation_prompt = """
        You are an expert financial advisor for decentralized finance (DeFi).
        You have access to the internet and many resources and live data on DeFi and Crypto.
        Your goal is to explain a pool recommendation in plain English, avoiding jargon where possible,
        the main goal is to make sure the user either a beginner or an expert understands the recommendation and about this pool.

        TASK: You will be given:
        1. A user's profile (experience level, goals).
        2. A pool's basic data (name, APY, etc.).
        3. Scores and other information that was calculated based off of the pool's metrics.

        USE THE INFORMATION GIVEN TO YOU AS MORE DATA TO ANSWER THE QUESTIONS, 
        Use especially all the information about the pools, the scores, risk scores, and more.
        Also you can serach the internet for more information, but they must be true and correspond with the pool you are working on


        Your task is to generate a clear, concise explanation (atleast 4 sentences) that includes:
        An explanation in Simple English for beginners, about this pool, 
        why it was recommended, and how it aligns with the user's profile. and wallet analysis.
        Include a brief summary of the pool's key metrics (APY, TVL, risks, etc.) and what they mean for the user.
        "Make sure to use userdata, pool data and metrics and scoring",
        add the risks, most important risks in simple terms.",
        And a final recommendation statement whether the user should consider this pool or not, and why.
        Keep the explanation factual and based on the data provided.

        YOUR RESPONSE MUST BE
        ALL PLAIN ENGLISH, NO ASTERICS, NO MARKDOWN, NO BULLETS, NO NUMBERS, NO JARGON.

        """
    
    def generate_explanation(self, user_profile: Dict[str, Any], 
                           pool_data: Dict[str, Any], 
                           score_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate human-readable explanation for a pool recommendation"""
        
        user_prompt = f"""

        1. User Profile:
        - Experience: {user_profile.get('experience_level', 'Beginner')}
        - Primary Goal: {user_profile.get('primary_goal', 'Make Steady Returns')}
        - Risk Tolerance: {user_profile.get('risk_tolerance', 'medium')}

        2. Pool Data:
        - Pool: {pool_data}
        
        3. Pool Metrics SCORE:
        - Scores: {score_result}

        """
        
        response = gemini_client.generate_structured_response(
            system_prompt=self.explanation_prompt,
            user_prompt=user_prompt
        )
        
        # Add metadata
        return response

# Global instance
explanation_engine = ExplanationEngine()

def create_sample_recommendation():
    """Example of how to use all three engines together"""
    
    # Sample data
    pool_data = {
        'chain': 'Ethereum', 
        'project': 'compound-v2', 
        'symbol': 'WBTC', 
        'tvlUsd': 253426158, 
        'apyBase': 0.00654, 
        'apyReward': 0, 
        'apy': 0.00654, 
        'rewardTokens': [], 
        'pool': '1d876729-4445-4623-8b6b-c5290db5d100', 
        'apyPct1D': 0, 'apyPct7D': 0, 'apyPct30D': -0.0009, 'stablecoin': False, 'ilRisk': 'no', 'exposure': 'single', 'predictions': {'predictedClass': 'Stable/Up', 'predictedProbability': 73, 'binnedConfidence': 2}, 'poolMeta': None, 'mu': 0.05035, 'sigma': 0.00475, 'count': 1323, 'outlier': False, 'underlyingTokens': ['0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599'], 'il7d': None, 'apyBase7d': None, 'apyMean30d': 0.00681, 'volumeUsd1d': None, 'volumeUsd7d': None, 'apyBaseInception': None
    }
    
    user_profile = {
        "experience_level": "beginner",
        "primary_goal": "earn steady, low-risk yield",
        "risk_tolerance": "low"
    }

    score_result = json.loads("""{
        "apy": 9.1423,
        "tvl_score": 100,
        "risk_score": "30.24%",
        "final_score": 28.52,
        "breakdown": {
            "tvl": "Liquidity: $2,655,534,964 \u2192 score 100",
            "impermanent_loss": "No",
            "stablecoin": "Stablecoin pool",
            "volatility_sigma": "0.003 (normalized 0.00)",
            "prediction_confidence": "82%",
            "exposure": "Single-asset",
            "explanation": "Pool appears relatively safe."
        },
        "pool": {
            "chain": "Ethereum",
            "project": "maple",
            "symbol": "USDC",
            "tvlUsd": 2655534964,
            "apyBase": 6.94231,
            "apyReward": 2.2,
            "apy": 9.14231,
            "rewardTokens": [
            "0x643C4E15d7d62Ad0aBeC4a9BD4b001aA3Ef52d66"
            ],
            "pool": "43641cf5-a92e-416b-bce9-27113d3c0db6",
            "apyPct1D": -0.03243,
            "apyPct7D": -0.13804,
            "apyPct30D": 6.94231,
            "stablecoin": true,
            "ilRisk": "no",
            "exposure": "single",
            "predictions": {
            "predictedClass": "Stable/Up",
            "predictedProbability": 82,
            "binnedConfidence": 3
            },
            "poolMeta": "Syrup USDC",
            "mu": 9.14109,
            "sigma": 0.00305,
            "count": 62,
            "outlier": false,
            "underlyingTokens": [
            "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
            ],
            "il7d": null,
            "apyBase7d": null,
            "apyMean30d": 9.26598,
            "volumeUsd1d": null,
            "volumeUsd7d": null,
            "apyBaseInception": null
        }
        }""")
    
    # Execute the pipeline
    explanation = explanation_engine.generate_explanation(user_profile, pool_data, score_result)
    
    
    return str(explanation)

data = create_sample_recommendation()

print(type(data))
print(data)