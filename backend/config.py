import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
    
    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL_TEXT = os.getenv("GEMINI_MODEL_TEXT", "gemini-1.5-flash")
    GEMINI_MODEL_IMAGE = os.getenv("GEMINI_MODEL_IMAGE", "gemini-2.0-flash")
    
    # Supabase Configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
    USE_SUPABASE = os.getenv("USE_SUPABASE", "True").lower() == "true"


settings = Settings()
