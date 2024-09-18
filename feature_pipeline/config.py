from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    EMBEDDING_MODEL_ID: str = "paraphrase-MiniLM-L6-v2"
    EMBEDDING_MODEL_MAX_INPUT_LENGTH: int = 512
    _file_path: str = 'MattFarmerAI-TikTok-Profile-Scripts-analytics.csv'