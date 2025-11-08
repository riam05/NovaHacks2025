"""
Political debate analyzer using OpenRouter API.
Generates arguments from both liberal and conservative perspectives.
"""
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_args(topic: str) -> tuple:
    """
    Generate API call arguments for political debate analysis.
    
    Args:
        topic: The political topic to analyze
        
    Returns:
        tuple: (headers dict, payload dict) for OpenRouter API call
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""Explain the current debate between liberals and conservatives on the topic: "{topic}". Don't be afraid to be opinionated.

Return **only valid JSON** describing both sides of the issue, with explicit stance labels. Use this schema exactly:
{{
  "topic": "{topic}",
  "sides": [
    {{
      "id": "A",
      "label": "liberal",
      "arguments": ["argument 1", "argument 2", ...],
      "sources": ["url1", "url2", ...]
    }},
    {{
      "id": "B",
      "label": "conservative",
      "arguments": ["argument 1", "argument 2", ...],
      "sources": ["url1", "url2", ...]
    }}
  ]
}}

Make sure all arguments are concise and supported by citations from RECENT sources."""
    
    payload = {
        "model": "perplexity/sonar-pro-search",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0
    }
    
    return headers, payload
