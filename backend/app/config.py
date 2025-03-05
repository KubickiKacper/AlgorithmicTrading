import os


class Config:
    DEBUG: bool = bool(os.environ.get("FLASK_DEBUG"))
    APP: str = str(os.environ.get("FLASK_APP"))
    RUN_PORT: int = int(os.environ.get("FLASK_RUN_PORT", 5000))
