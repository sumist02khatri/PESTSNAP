from functools import lru_cache

from ultralytics import YOLO

from config.settings import MODEL_PATH


@lru_cache(maxsize=1)
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model weights not found at {MODEL_PATH}")
    return YOLO(str(MODEL_PATH))
