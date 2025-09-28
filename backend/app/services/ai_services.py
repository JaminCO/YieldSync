from typing import Dict, Any, Optional
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from app.services.utils import GeminiClient, ExplanationEngine

load_dotenv()

def create_sample_recommendation(user_profile, pool_data, score_result) -> str:
    """Example of how to use all three engines together"""

    # Initialize the engines
    gemini_client = GeminiClient()
    explanation_engine = ExplanationEngine()

    # Execute the pipeline
    explanation = explanation_engine.generate_explanation(user_profile, pool_data, score_result)
    
    
    return str(explanation)


