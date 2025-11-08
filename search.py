import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
AIRIA_API_KEY = os.getenv("AIRIA_API_KEY")

def generate_args(topic):
    """Generate the arguments for the API call"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
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
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0
    }
    
    return headers, payload

topic = "The current U.S. government shutdown debate"
headers, payload = generate_args(topic)

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers=headers,
    data=json.dumps(payload)
)

data = response.json()

os.makedirs("results", exist_ok=True)
output_path = os.path.join("results", "government_shutdown.json")

with open(output_path, "w") as f:
    json.dump(data, f, indent=2)

# Extract the JSON content from the response
content = data["choices"][0]["message"]["content"]
debate_json = json.loads(content)

# Send the JSON to Airia API
AIRIA_ENDPOINT = "https://api.airia.ai/v2/PipelineExecution/4f07f9ed-1e9a-4747-9de3-8bfa84e4c36a"

airia_headers = {
    "Content-Type": "application/json"
}

# Add API key to headers if available
if AIRIA_API_KEY:
    airia_headers["Authorization"] = f"Bearer {AIRIA_API_KEY}"

print(f"Sending JSON to Airia API: {AIRIA_ENDPOINT}")
airia_response = requests.post(
    AIRIA_ENDPOINT,
    headers=airia_headers,
    json=debate_json
)

print(f"Airia API Response Status: {airia_response.status_code}")
print(f"Airia API Response: {airia_response.text}")

if airia_response.status_code == 200:
    print("Successfully sent JSON to Airia!")
else:
    print(f"Error sending to Airia: {airia_response.status_code}")
