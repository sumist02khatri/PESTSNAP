# Rice Pest Classification App

Production-ready Streamlit application for rice pest image classification using a YOLOv8 classification model, with pest recommendations and chatbot modes for both local development and cloud hosting.

## Features

- Image upload and classification using `modal/best.pt`
- Predicted pest class and confidence score
- Recommendation system with problem, cure, and prevention guidance
- Chat assistant modes:
  - `Fast mode` for rule-based offline responses
  - `Local Ollama mode` using the smaller `llama3.2:1b` model by default
  - `Free Cloud mode` using Groq's API
- Hosted mode support that hides `Local Ollama mode` for lighter deployments
- Modular separation for UI components, utilities, and root config
- Docker-ready deployment

## Folder Structure

```text
PESTSNAP/
|-- app/
|   |-- app.py
|   |-- components/
|   |   |-- chatbot.py
|   |   |-- prediction.py
|   |   |-- recommendation.py
|   |   `-- uploader.py
|   `-- utils/
|       |-- llm_handler.py
|       |-- model_loader.py
|       `-- pest_info.py
|-- config/
|   `-- settings.py
|-- modal/
|   `-- best.pt
|-- .dockerignore
|-- .env.example
|-- classes.txt
|-- docker-compose.yml
|-- Dockerfile
|-- README.md
|-- requirements.txt
`-- run.sh
```

## Deployment Modes

### Local mode

Use:
- `Fast mode`
- `Local Ollama mode`
- `Free Cloud mode`

Set:

```env
DEPLOYMENT_MODE=local
```

### Cloud mode

Use:
- `Fast mode`
- `Free Cloud mode`

`Local Ollama mode` is hidden automatically.

Set:

```env
DEPLOYMENT_MODE=cloud
```

## Where To Change The Ollama Model

The default local model is set in `config/settings.py`:

```python
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
```

You can change it in either of these ways:

1. Temporary for one terminal session:

```powershell
$env:OLLAMA_MODEL="llama3.2:1b"
```

2. Permanent default in code:

Update the fallback value in `config/settings.py`.

## Local Run

From the project root:

```bash
pip install -r requirements.txt
streamlit run app/app.py --server.port 8502
```

Open `http://localhost:8502`

## Local Environment File

Create `.env` in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
OLLAMA_MODEL=llama3.2:1b
DEPLOYMENT_MODE=local
```

The app auto-loads `.env` on local startup.

## Ollama Setup

Install Ollama locally, then run:

```bash
ollama pull llama3.2:1b
```

The app defaults to:

```text
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:1b
```

If Ollama is unavailable, the app automatically falls back to curated rule-based guidance.

## Groq Setup

Add your Groq API key to `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

If the API key is missing or the request fails, the app falls back to curated pest guidance.

## Docker For Local Full Stack

Use Docker Compose only if you want both:
- app in Docker
- Ollama in Docker

Start both containers:

```bash
docker compose up --build -d
```

Pull the Ollama model inside the running Ollama container:

```bash
docker exec -it pestsnap-ollama ollama pull llama3.2:1b
```

Then open:

```text
http://localhost:8501
```

## Docker For Hosting

For free-tier hosting, deploy only the app container from `Dockerfile`.

The Docker image now defaults to:

```text
DEPLOYMENT_MODE=cloud
```

so hosted deployments automatically hide `Local Ollama mode`.

Build locally:

```bash
docker build -t pestsnap-app .
```

Run locally in a hosting-like way:

```bash
docker run --rm -p 8501:8501 --env-file .env -e DEPLOYMENT_MODE=cloud pestsnap-app
```

Recommended hosting env vars:

```text
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
DEPLOYMENT_MODE=cloud
DEFAULT_CHAT_MODE=Fast mode
```

Do not depend on Ollama for free-tier hosting.

## Notes

- Local development can keep all three chatbot modes.
- Free-tier hosting should use only `Fast mode` and `Free Cloud mode`.
- The app container can be deployed to platforms like Render or Railway using the root `Dockerfile`.
