import os
import json
from typing import Dict, Any, Optional
import re
# import google.generativeai as genai
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    """Client for interacting with Google Gemini API"""

    def __init__(self, api_key: Optional[str] = "AIzaSyCVKCq4QYU4Z8eUqjDls6h_--3UUAbIUg8"):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        # genai.configure(api_key=self.api_key)
        # self.model = genai.GenerativeModel('gemini-2.5-pro')
        self.client = genai.Client()
        
    def generate_structured_response(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """
        Generate structured response from Gemini with error handling
        """
        try:
            # Generate content
            response = self.client.models.generate_content(
                model="gemini-2.5-pro",
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt
                ),
                contents=user_prompt
            )

            response_text = response.text.strip()
            
            return response_text

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response from Gemini: {e}")
        except Exception as e:
            raise

# Singleton instance
gemini_client = GeminiClient()

class PersonalizationEngine:
    """Generates human-readable explanations for pool recommendations"""
    
    def __init__(self):
        self.gemini_client = GeminiClient()
        self.explanation_prompt = """
        You are a personalized DeFi financial advisor. Your role is to explain pool recommendations in clear, simple language that matches each user's experience level.

        TASK: Create personalized investment explanations using:
        1. User's profile, goals, and risk tolerance
        2. Pool data and metrics (APY, TVL, audit status, etc.)
        3. Calculated scores and risk assessments

        CRITICAL RULES:
        - Write in complete sentences only - NO bullets, numbers, markdown, or asterisks
        - Use plain English that beginners can understand
        - Include specific numbers in brackets like this: (4.5%), ($1.2 billion), (85/100)
        - Keep explanations factual and data-driven
        - Always connect pool features to user's specific situation

        REQUIRED CONTENT STRUCTURE:
        1. Start with how this pool matches the user's goals and experience level
        2. Explain key metrics and what they mean for the user personally
        3. Describe the most important risks in simple terms
        4. End with clear recommendation: whether to consider this pool and why

        Remember to use all provided data - pool metrics, risk scores, and user preferences - to create truly personalized advice.
        """
        
        self.action_prompt = """
        You are a DeFi investment advisor. Analyze pool data AND user profile to provide a one-word action recommendation.

        TASK: Based on comprehensive analysis of both the pool data AND user profile, output only one word:
        - "Invest" if the pool matches the user's goals, risk tolerance, and appears safe
        - "Avoid" if the pool doesn't match user preferences or appears too risky for them

        Consider both factors: pool safety metrics AND user's specific situation, goals, and risk tolerance.

        CRITICAL RULES:
        - Output exactly one word: "Invest" or "Avoid"
        - No explanations, no additional text, no formatting
        - Base decision on the combination of pool metrics and user profile suitability
        """
    
    def generate_explanation(self, 
                           user_profile: Dict[str, Any],
                           pool_data: Dict[str, Any], 
                           score_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate human-readable explanation for a pool recommendation"""
        
        user_prompt = f"""

        You are given the following information:
        1. User Profile:
        - Profile: {user_profile}

        2. Pool Data:
        - Pool: {pool_data}

        3. Pool Metrics SCORE:
        - Scores: {score_result}

        """

        response = self.gemini_client.generate_structured_response(
            system_prompt=self.explanation_prompt,
            user_prompt=user_prompt
        )
        
        # Add metadata
        return response

    def generate_action(self,
                           user_profile: Dict[str, Any],
                           pool_data: Dict[str, Any], 
                           score_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate human-readable explanation for a pool recommendation"""
        
        user_prompt = f"""
        You are given the following information:
        1. User Profile:
        - Profile: {user_profile}

        2. Pool Data:
        - Pool: {pool_data}

        3. Pool Metrics SCORE:
        - Scores: {score_result}

        One word action based on the above information, either "Invest" or "Avoid".
        """

        response = self.gemini_client.generate_structured_response(
            system_prompt=self.action_prompt,
            user_prompt=user_prompt
        )

        # Add metadata
        return response



# Global instance
explanation_engine = PersonalizationEngine()

def create_sample_recommendation():
    """Example of how to use all three engines together"""
    
    # Sample data
    pool_data = json.loads("""{
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
        }""")
    
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

    user_profile = {
        "name": "Alice",
        "experience_level": "beginner",
        "investment_goals": "steady income with low risk",
        "risk_tolerance": "low",
        "preferred_chains": ["Ethereum", "Polygon"],
        "preferred_projects": ["maple", "aave"],
        "disliked_projects": ["uniswap"]
    }
    
    # Execute the pipeline
    explanation = explanation_engine.generate_explanation(user_profile, pool_data, score_result)

    action = explanation_engine.generate_action(user_profile, pool_data, score_result)


    return [str(explanation), action]

data = create_sample_recommendation()

print(data)