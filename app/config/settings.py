from pathlib import Path
import os


APP_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = APP_DIR / "modal" / "best.pt"
CLASSES_PATH = APP_DIR / "classes.txt"

APP_TITLE = "Rice Pest Classification Assistant"
APP_ICON = "🌾"
APP_LAYOUT = "wide"

STREAMLIT_HOST = os.getenv("STREAMLIT_SERVER_ADDRESS", "0.0.0.0")
STREAMLIT_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

DEFAULT_CHAT_MODE = os.getenv("DEFAULT_CHAT_MODE", "Fast mode")
ALLOWED_CHAT_MODES = ("Fast mode", "Local Ollama mode", "Free Cloud mode")

MAX_IMAGE_SIZE_MB = 10
