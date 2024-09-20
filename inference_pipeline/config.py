from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):

    # Embeddings config
    EMBEDDING_MODEL_ID: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_MODEL_MAX_INPUT_LENGTH: int = 256
    EMBEDDING_SIZE: int = 384
    EMBEDDING_MODEL_DEVICE: str = "cpu"
    _file_path: str = 'sdb/dataset.csv'

    OPENAI_MODEL_ID: str = "gpt-4-1106-preview"
    OPENAI_API_KEY: str = "sk--wgT5Os0yh65yiaLY39ycJii98y9zQ6Y4alSi4dQ48T3BlbkFJHZHitsUUCDO48X3MDSWMFdtpeotEy71XvyQMBpf8cA"

    # QdrantDB config
    QDRANT_DATABASE_HOST: str = "localhost"
    QDRANT_DATABASE_PORT: int = 6333
    QDRANT_DATABASE_URL: str = "http://localhost:6333"
    QDRANT_CLOUD_URL: str = "str"
    USE_QDRANT_CLOUD: bool = False
    QDRANT_APIKEY: str | None = None

settings = AppSettings()
