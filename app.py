import os
import json
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from search import generate_args

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TopicRequest(BaseModel):
    topic: str

@app.post('/api/analyze')
async def analyze_topic(request: TopicRequest):
    """API endpoint to analyze a political topic"""
    topic = request.topic
    
    if not topic:
        raise HTTPException(status_code=400, detail="Topic is required")
    
    try:
        # Generate API call arguments
        headers, payload = generate_args(topic)
        
        # Make the API call
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )
        
        result = response.json()
        
        # Save results
        os.makedirs("results", exist_ok=True)
        safe_filename = "".join(c if c.isalnum() else "_" for c in topic.lower())
        output_path = os.path.join("results", f"{safe_filename}.json")
        
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)
        
        return {
            "success": True,
            "data": result,
            "saved_to": output_path
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/health')
async def health():
    """Health check endpoint"""
    return {"status": "ok"}

