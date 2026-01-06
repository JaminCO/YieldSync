import os
import json
from typing import Dict, Any, Optional
import re
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
        self.client = genai.Client()
        
    def generate_structured_response(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """
        Generate structured response from Gemini with error handling
        """
        try:
            # Generate content
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
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


class ExplanationEngine:
    """Generates human-readable explanations for pool recommendations"""
    
    def __init__(self):
        self.gemini_client = GeminiClient()
        self.explanation_prompt = """
        You are an expert financial advisor for decentralized finance (DeFi).
        You have access to the internet and many resources and live data on DeFi and Crypto.
        Your goal is to explain a pool recommendation in plain English, avoiding jargon where possible,
        the main goal is to make sure the user either a beginner or an expert understands the recommendation and about this pool.

        TASK: You will be given:
        1. A pool's basic data (name, APY, etc.).
        2. Scores and other information that was calculated based off of the pool's metrics.

        USE THE INFORMATION GIVEN TO YOU AS MORE DATA TO ANSWER THE QUESTIONS, 
        Use especially all the information about the pools, the scores, risk scores, and more.
        Also you can search the internet for more information, but they must be true and correspond with the pool you are working on


        Your task is to generate a clear, concise explanation (atleast 4 sentences) that includes:
        An explanation in Simple English for beginners, about this pool, 
        Include a brief summary of the pool's key metrics (APY, TVL, risks, etc.) and what they mean for the user.
        "Make sure to use pool data and metrics and scoring",
        add the risks, most important risks in simple terms.",
        And a final recommendation statement whether the user should consider this pool or not, and why.
        Keep the explanation factual and based on the data provided.

        RULES:
        - YOUR RESPONSE MUST BE.
        - ALL PLAIN ENGLISH, NO ASTERISKS, NO MARKDOWN, NO BULLETS, NO NUMBERS, NO JARGON.
        - WHEN CALLING OUT NUMBERS ADD THE FIGURES IN BRACKETS, I.E. (5%), (100,000 USD), (20)
        """
        
        self.action_prompt = """
        You are an expert financial advisor for decentralized finance (DeFi).
        You have access to the internet and many resources and live data on DeFi and Crypto.
        Your goal is to provide a one-word action recommendation based on the pool's data and your analysis.

        TASK: Based on the pool's data and your analysis, provide a one-word action recommendation:
        - If you think the user should invest in the pool, respond with "Invest".
        - If you think the user should avoid the pool, respond with "Avoid".

        Your response must be based on the data provided and your understanding of the DeFi landscape.

        RULES:
        - YOUR RESPONSE MUST BE.
        - ALL PLAIN ENGLISH, NO ASTERISKS, NO MARKDOWN, NO BULLETS, NO NUMBERS, NO JARGON.
        """
    
    def generate_explanation(self, 
                           pool_data: Dict[str, Any], 
                           score_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate human-readable explanation for a pool recommendation"""
        
        user_prompt = f"""

        You are given the following information:
        1. Pool Data:
        - Pool: {pool_data}

        2. Pool Metrics SCORE:
        - Scores: {score_result}

        """

        response = self.gemini_client.generate_structured_response(
            system_prompt=self.explanation_prompt,
            user_prompt=user_prompt
        )
        
        # Add metadata
        return response

    def generate_action(self, 
                           pool_data: Dict[str, Any], 
                           score_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate human-readable explanation for a pool recommendation"""
        
        user_prompt = f"""
        You are given the following information:
        1. Pool Data:
        - Pool: {pool_data}

        2. Pool Metrics SCORE:
        - Scores: {score_result}

        One word action based on the above information, either "Invest" or "Avoid".
        """

        response = self.gemini_client.generate_structured_response(
            system_prompt=self.action_prompt,
            user_prompt=user_prompt
        )

        # Add metadata
        return response

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
        - "Invest" if the pool matches the user's goals, risk tolerance, and appears safe, and AI generation details support investment
        - "Avoid" if the pool doesn't match user preferences or appears too risky for them

        Consider both factors: pool safety metrics AND user's specific situation, goals, and risk tolerance, AI generation details and Information from the internet.

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

class WalletAnalyzer:
    def __init__(self):
        self.gemini_client = GeminiClient()
        self.prompt = """ You are an AI Blockchain Analyst. Analyze the user's on-chain data and produce a structured JSON 
        containing wallet activity insights. Use the data to assess behavior, diversity, and potential risk.
        You will be given a dict with transaction_list, token_transfer_list, and more information about the wallet.
        Your task is to return ONLY a valid JSON object with these keys:

        {{
            "score": integer - from 0 to 100 based on activity, diversity, and token behavior",
            "last_active": "ISO datetime of last transaction or token transfer",
            "ai_recommendation": "1–2 sentence actionable insight for the wallet owner",
            "top_tokens": "comma-separated list of top tokens held or transferred",
            "risk_profile": "Low / Medium / High based on unusual or spammy patterns",
            "common_token_types": "summary of types (e.g. stablecoins, DeFi, NFTs, meme tokens)",
            "portfolio_summary": "a human-readable paragraph summarizing portfolio history and activity"
        }}
        """

    def clean_json_response(self, response_text):
        """Clean and extract valid JSON from AI response."""
        import re
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if not json_match:
            print("⚠️ No JSON object found in response")
            return None

        json_str = json_match.group()
        json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)  # trailing commas fix

        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            print("Could not parse JSON")
            return None

    def analyze_wallet(self, wallet_data):
        """
        wallet_data: dict with transaction_list, token_transfer_list, etc.
        Returns AI-generated structured wallet profile
        """
        user_prompt = f"""
        wallet_data: {wallet_data}
        """

        try:
            response = self.gemini_client.generate_structured_response(
                system_prompt=self.prompt,
                user_prompt=user_prompt
            )

            return self.clean_json_response(response)
        except Exception as e:
            print(f"AI Error: {e}")
            return None