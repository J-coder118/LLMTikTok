from sentence_transformers.SentenceTransformer import SentenceTransformer

from config import settings


def embedd_text(text: str):
    model = SentenceTransformer(settings.EMBEDDING_MODEL_ID)
    return model.encode(text)
