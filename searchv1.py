import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
AIRIA_API_KEY = os.getenv("AIRIA_API_KEY")
AIRIA_ENDPOINT = "https://api.airia.ai/v2/PipelineExecution/4f07f9ed-1e9a-4747-9de3-8bfa84e4c36a"


def generate_debate_json(topic, openrouter_key):
    headers = {
        "Authorization": f"Bearer {openrouter_key}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
Explain the current debate between liberals and conservatives on the topic: "{topic}". Don't be afraid to be opinionated.
Return **only valid JSON** describing both sides of the issue, with explicit stance labels. Use this schema exactly:
{{
  "topic": "{topic}",
  "sides": [
    {{
      "id": "A",
      "label": "liberal",
      "arguments": ["arguments for a liberal side", ...],
      "sources": ["url1", "url2", ...]
    }},
    {{
      "id": "B",
      "label": "conservative",
      "arguments": ["arguments for a conservative side", ...],
      "sources": ["url1", "url2", ...]
    }}
  ]
}}
Make sure all arguments are concise and supported by citations.
"""
    
    payload = {
        "model": "perplexity/sonar-pro-search",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0
    }
    
    print(f"Generating debate JSON for: {topic}")
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )
    
    data = response.json()
    
    os.makedirs("results", exist_ok=True)
    output_path = os.path.join("results", "government_shutdown.json")
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Raw response saved to {output_path}")
    
    content = data["choices"][0]["message"]["content"]
    
    if '```json' in content:
        content = content.split('```json')[1].split('```')[0].strip()
    elif '```' in content:
        content = content.split('```')[1].split('```')[0].strip()
    
    debate_json = json.loads(content)
    
    debate_output_path = os.path.join("results", "debate_cleaned.json")
    with open(debate_output_path, "w") as f:
        json.dump(debate_json, f, indent=2)
    
    print(f"Cleaned debate JSON saved to {debate_output_path}")
    
    return debate_json


def send_to_airia(debate_json, airia_key, airia_endpoint):
    headers = {
        "Content-Type": "application/json"
    }
    
    if airia_key:
        headers["Authorization"] = f"Bearer {airia_key}"
    
    print(f"Sending JSON to Airia API: {airia_endpoint}")
    
    response = requests.post(
        airia_endpoint,
        headers=headers,
        json=debate_json
    )
    
    print(f"Airia API Response Status: {response.status_code}")
    
    airia_output_path = os.path.join("results", "airia_response.json")
    with open(airia_output_path, "w") as f:
        json.dump({
            "status_code": response.status_code,
            "response": response.text
        }, f, indent=2)
    
    print(f"Airia response saved to {airia_output_path}")
    
    return response


def main():
    topic = "The current U.S. government shutdown debate"
    
    print("Starting Automated Pipeline")
    
    debate_json = generate_debate_json(topic, API_KEY)
    
    print("Debate JSON Preview:")
    print(json.dumps(debate_json, indent=2)[:500] + "...")
    
    response = send_to_airia(debate_json, AIRIA_API_KEY, AIRIA_ENDPOINT)
    
    if response.status_code == 200:
        print("SUCCESS: JSON sent to Airia")
        print(f"Response: {response.text[:200]}")
    else:
        print("FAILURE")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")


if __name__ == "__main__":
    main()