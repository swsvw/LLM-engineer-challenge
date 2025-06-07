# LLM-engineer-challenge

PrivChat - PII Detection System

<img width="1433" alt="Screenshot 2025-06-08 at 1 58 06 AM" src="https://github.com/user-attachments/assets/f2124cf9-a2de-4247-bb39-447544e11e16" />

https://github.com/user-attachments/assets/f7c5fcf8-0620-4443-a29b-9fa609b88835

<img width="1433" alt="Screenshot 2025-06-08 at 2 02 54 AM" src="https://github.com/user-attachments/assets/a3056ff4-3ad6-4eef-9b52-53f2d6820f1d" /><img width="1433" alt="Screenshot 2025-06-08 at 2 05 32 AM" src="https://github.com/user-attachments/assets/cb044c3e-1f21-4fbe-9c32-e640c00167d0" />



A privacy-focused chat application that detects and sanitizes Personally Identifiable Information (PII) before sending messages to Large Language Models (LLMs).
🎯 Features

    Real-time PII Detection: Uses spaCy NER to identify personal information
    Visual Highlighting: Color-coded highlighting of different PII types
    Privacy Protection: Sanitizes messages before sending to LLM
    Local LLM Integration: Works with Ollama for private AI processing
    Modern UI: Mac-style interface with smooth animations
    Multiple Chat Spaces: Organize conversations in different contexts

🛠 Technology Stack

    Backend: FastAPI with Python 3.8+
    NER: spaCy with en_core_web_sm model
    LLM: Ollama REST API (supports various models)
    Frontend: Vanilla HTML/CSS/JavaScript
    API: RESTful with automatic documentation

📋 Prerequisites

    Python 3.8+
    Ollama - Download from ollama.ai
    Modern web browser

🚀 Quick Start
Option 1: Automatic Setup (Recommended)

bash

# Make setup script executable
chmod +x setup.sh

# Run setup script
./setup.sh

Option 2: Manual Setup

    Clone and setup Python environment:

bash

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm

    Install and setup Ollama:

bash

# Install Ollama from https://ollama.ai
ollama pull llama2  # or your preferred model
ollama serve        # Start Ollama server

    Start the FastAPI server:

bash

python main.py

    Open the frontend:
        Open index.html in your web browser
        Or serve it with a local server: python -m http.server 3000

🔧 Configuration
Changing the LLM Model

Edit main.py and change the DEFAULT_MODEL variable:

python

DEFAULT_MODEL = "llama2"  # Change to your preferred model

Available models can be listed with: ollama list
API Configuration

The frontend connects to http://localhost:8000 by default. To use a different URL, edit the API_BASE_URL in index.html.
📡 API Endpoints
POST /chat

Process a chat message with PII detection and LLM response.

Request:

json

{
    "prompt": "Hello, my name is John Doe",
    "chat_space": 1
}

Response:

json

{
    "original_prompt": "Hello, my name is John Doe",
    "detected_entities": [
        {
            "text": "John Doe",
            "label": "PERSON",
            "start": 18,
            "end": 26,
            "confidence": 0.95
        }
    ],
    "sanitized_prompt": "Hello, my name is [PERSON]",
    "llm_response": "Hello! Nice to meet you...",
    "processing_time": 2.34
}

GET /health

Check API health and dependencies.
GET /models

List available Ollama models.
🎨 PII Detection Types

The system detects and highlights various PII types:

Type	Color	Examples
Person Names	🟠 Orange	John Doe, Jane Smith
Locations	🔵 Blue	New York, California
Organizations	🟣 Purple	Microsoft, Google
Miscellaneous	🟢 Green	Dates, Money, Percentages

🖥 Usage Examples
Example 1: Basic PII Detection

Input: "My name is John Doe and I work at Microsoft in Seattle."
Detected: John Doe (PERSON), Microsoft (ORG), Seattle (GPE)
Sanitized: "My name is [PERSON] and I work at [ORG] in [GPE]."

Example 2: Contact Information

Input: "Contact sarah.johnson@email.com at (555) 123-4567"
Detected: Email and phone patterns (if configured)

🔒 Privacy Features

    Local Processing: All PII detection happens locally
    Sanitization: Personal data is replaced with placeholders before LLM processing
    No Data Storage: No conversation data is stored permanently
    Offline Capable: Works with local LLM models

🧪 Testing
Console Output

The system logs detected entities and LLM responses to the browser console:

javascript

// Open browser developer tools to see:
🔍 DETECTED ENTITIES:
1. John Doe (PERSON) - Confidence: 95%
2. New York (GPE) - Confidence: 88%

🤖 LLM RESPONSE:
Hello! I'd be happy to help you with your request...

⏱️ Processing Time: 2.34s

Sample Test Cases

    Names and Locations: "John Doe lives in New York City"
    Organizations: "I work at Google in Mountain View"
    Mixed PII: "Contact Dr. Smith at Stanford University"
    No PII: "What's the weather like today?"

🚨 Troubleshooting
Common Issues

    "spaCy model not found"

    bash

    python -m spacy download en_core_web_sm

    "Ollama connection failed"
        Ensure Ollama is running: ollama serve
        Check if models are available: ollama list
    "CORS errors in browser"
        Serve the HTML file through a web server instead of opening directly
        Use: python -m http.server 3000
    API not responding
        Check if FastAPI is running on port 8000
        Visit http://localhost:8000/docs for API documentation

Debug Mode

Start the API with debug logging:

bash

uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level debug

📁 Project Structure

privchat-pii-detection/
├── main.py                 # FastAPI backend
├── requirements.txt        # Python dependencies  
├── index.html             # Frontend application
├── setup.sh               # Installation script
├── README.md              # This file
└── screenshots/           # Demo screenshots
    ├── main-interface.png
    ├── pii-detection.png
    └── console-output.png

🎯 System Requirements Met

✅ Prompt Input: Text area for user input
✅ FastAPI Backend: RESTful API with automatic docs
✅ spaCy NER: Named entity recognition with en_core_web_sm
✅ Ollama Integration: Local LLM via REST API
✅ Console Logging: Entities and responses printed to console
✅ Visual Display: PII highlighting and LLM response in GUI
✅ Clean Code: Organized, documented, and modular
🚀 Deployment

For production deployment:

    Set proper CORS origins in main.py
    Use a production ASGI server like Gunicorn
    Set up SSL/TLS certificates
    Configure firewall rules
    Use environment variables for configuration

📄 License

This project is created for the LLM Engineer coding challenge.
🤝 Contributing

This is a coding challenge submission. For questions or improvements, please refer to the interview process.

Demo Time: ~2-3 hours implementation
Tech Stack: FastAPI + spaCy + Ollama + Vanilla JS
Focus: Functional completeness with clean, organized code
