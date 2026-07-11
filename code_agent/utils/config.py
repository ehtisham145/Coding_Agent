from pydantic_settings import BaseSettings
import logging
from openai import OpenAI
from pathlib import Path

#----------Logging Setup--------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("coding_agent")


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o"
    MAX_TOKENS_RESPONSE: int = 8096
    MAX_TOOL_OUTPUT_CHARS: int = 8000

    class Config:
        env_file = Path.home() / ".coding_agent" / ".env"

#----------------Initialize Settings--------------------------

try:
    settings = Settings()

except Exception as e:
    logger.critical(f"Failed to Load Settings Check your .env File Error : {e}")
    raise SystemExit(1)


#----------------Initialize OpenAI Client--------------------------

try:
    llm_client = OpenAI(api_key=settings.OPENAI_API_KEY)

except Exception as e:
    logger.critical(f"Failed to initialize OpenAI client: {e}")
    raise SystemExit(1)