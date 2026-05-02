from pathlib import Path
import os

from dotenv import load_dotenv


APP_DIR = Path(__file__).resolve().parent.parent
load_dotenv(APP_DIR / ".env")

MODEL_PATH = APP_DIR / "modal" / "best.pt"
CLASSES_PATH = APP_DIR / "classes.txt"

APP_TITLE = "PESTSNAP - Rice Pest Classification Assistant"
APP_ICON = "🌾"
APP_LAYOUT = "wide"
DEPLOYMENT_MODE = os.getenv("DEPLOYMENT_MODE", "local").strip().lower()

STREAMLIT_HOST = os.getenv("STREAMLIT_SERVER_ADDRESS", "0.0.0.0")
STREAMLIT_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

DEFAULT_CHAT_MODE = os.getenv("DEFAULT_CHAT_MODE", "Fast mode")
if DEPLOYMENT_MODE == "cloud":
    ALLOWED_CHAT_MODES = ("Fast mode", "Free Cloud mode")
else:
    ALLOWED_CHAT_MODES = ("Fast mode", "Local Ollama mode", "Free Cloud mode")

MAX_IMAGE_SIZE_MB = 10
