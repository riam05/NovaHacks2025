# Political Debate Analyzer

A web application that analyzes political topics and presents both liberal and conservative perspectives using AI.

## Features

- 🎨 Beautiful landing page built with React, TypeScript, and Tailwind CSS
- 🔍 Powered by Perplexity's Sonar Pro Search for real-time analysis
- 📊 Presents both sides of political debates with sources
- 🔐 Secure API key management with environment variables

## Tech Stack

**Frontend:**
- React
- TypeScript
- Tailwind CSS

**Backend:**
- FastAPI (Python)
- OpenRouter API (Perplexity Sonar Pro Search)

## Setup Instructions

### 1. Install Dependencies

**Backend:**
```bash
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:
```
OPENROUTER_API_KEY=your_api_key_here
```

### 3. Run the Application

**Terminal 1 - Start Backend:**
```bash
uvicorn app:app --reload
```
Backend will run on `http://localhost:8000`

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm start
```
Frontend will run on `http://localhost:3000`

### 4. Use the App

1. Open `http://localhost:3000` in your browser
2. Enter a political topic (e.g., "government shutdown", "climate policy")
3. Click to analyze
4. View the results with arguments from both sides

## Project Structure

```
NovaHacks2025/
├── app.py                 # FastAPI backend API
├── search.py             # Original search script
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
├── results/              # Saved analysis results
└── frontend/             # React frontend
    ├── src/
    │   ├── App.tsx       # Main landing page component
    │   └── index.css     # Tailwind CSS
    └── package.json      # Node dependencies
```

## API Endpoints

- `POST /api/analyze` - Analyze a political topic
- `GET /api/health` - Health check
- Interactive API docs: `http://localhost:8000/docs`

## Security Note

Never commit your `.env` file or expose your API keys. The `.gitignore` is configured to exclude sensitive files.
