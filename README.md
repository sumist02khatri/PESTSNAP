# Rice Pest Classification App

Production-ready Streamlit application for rice pest image classification using a YOLOv8 classification model, with pest recommendations and three chatbot modes.

## Features

- Image upload and classification using `modal/best.pt`
- Predicted pest class and confidence score
- Recommendation system with problem, cure, and prevention guidance
- Chat assistant modes:
  - `Fast mode` for rule-based offline responses
  - `Local Ollama mode` for offline LLM responses using `llama3`
  - `Free Cloud mode` using Groq's API
- Modular project structure for UI, config, and utilities
- Docker-ready deployment on port `8501`

## Folder Structure

```text
app/
├── app.py
├── classes.txt
├── Dockerfile
├── README.md
├── requirements.txt
├── run.sh
├── components/
│   ├── chatbot.py
│   ├── prediction.py
│   ├── recommendation.py
│   └── uploader.py
├── config/
│   └── settings.py
├── modal/
│   └── best.pt
└── utils/
    ├── llm_handler.py
    ├── model_loader.py
    └── pest_info.py
```

## Local Run

```bash
cd app
pip install -r requirements.txt
streamlit run app.py --server.port 8501
```

Open `http://localhost:8501`

## Ollama Setup

Install Ollama locally, then run:

```bash
ollama serve
ollama pull llama3
```

Optional environment variables:

```bash
set OLLAMA_BASE_URL=http://localhost:11434
set OLLAMA_MODEL=llama3
```

If Ollama is unavailable, the app automatically falls back to curated rule-based guidance.

## Free Cloud Setup with Groq

Create a Groq API key and export it before running the app:

```bash
set GROQ_API_KEY=your_api_key_here
set GROQ_MODEL=llama-3.3-70b-versatile
```

If the API key is missing or the request fails, the app falls back to curated pest guidance.

Groq Python integration is based on the official Groq docs for chat completions:
- https://console.groq.com/docs/text-chat
- https://console.groq.com/docs/api-reference

## Docker

Build from the `app` directory:

```bash
cd app
docker build -t pestsnap-app .
docker run --rm -p 8501:8501 pestsnap-app
```

To use Ollama from Docker on Docker Desktop, point the app to the host:

```bash
docker run --rm -p 8501:8501 -e OLLAMA_BASE_URL=http://host.docker.internal:11434 pestsnap-app
```

To use Groq in Docker:

```bash
docker run --rm -p 8501:8501 -e GROQ_API_KEY=your_api_key_here pestsnap-app
```

The container listens on `8501`, so it does not clash with services already using `5432`.
