from pydantic_settings import BaseSettings
import logging
from groq import Groq

#----------Logging Setup--------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("coding_agent")



class Settings(BaseSettings):
    GROQ_API_KEY : str
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    AX_TOKENS_RESPONSE: int = 4096
    MAX_TOOL_OUTPUT_CHARS: int = 4000  


    class Config:
        env_file = ".env"
    
#----------------Initialize  Settings--------------------------

try: 
    settings = Settings()

except Exception as e:
    logger.critical(f"Failed to Load Settings Check your .env File Error : {e}")
    raise SystemExit(1)



#----------------Initialize Groq Client--------------------------
try: 
    groq_client = Groq(api_key=settings.GROQ_API_KEY)

except Exception as e:
    logger.critical(f"Failed to initialize Groq client: {e}")
    raise SystemExit(1)