import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class AppConfig(BaseModel):
    BANK_NAME: str = "NEXUS International Banking Corp."
    VERSION: str = "1.0.0"
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEFAULT_LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "cognitive")  # cognitive | gemini | openai
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ENABLE_GUARDRAILS: bool = True
    ENABLE_PII_MASKING: bool = True
    TOKEN_BUDGET_PER_REQUEST: int = 4096
    DEFAULT_CUSTOMER_ID: str = "CUST-1001"

config = AppConfig()
