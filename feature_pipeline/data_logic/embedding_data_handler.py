from abc import ABC, abstractmethod

from model.base import DataModel
from model.chunk import TikTokProfileChunkModel
from model.embedded_chunk import (
    TikTokProfileEmbeddedChunkModel
)
from utils.embeddings import embedd_text


class EmbeddingDataHandler(ABC):
    """
    Abstract class for all embedding data handlers.
    All data transformations logic for the embedding step is done here
    """

    @abstractmethod
    def embedd(self, data_model: DataModel) -> DataModel:
        pass


class TikTokProfileEmbeddingHandler(EmbeddingDataHandler):
    def embedd(self, data_model: TikTokProfileChunkModel) -> TikTokProfileEmbeddedChunkModel:
        return TikTokProfileEmbeddedChunkModel(
            entry_id=data_model.entry_id,
            views=data_model.views,
            comments=data_model.comments,
            shares=data_model.shares,
            likes=data_model.likes,
            bookmark=data_model.bookmark,
            duration=data_model.duration,
            url=data_model.url,
            caption=data_model.caption,
            chunk_id=data_model.chunk_id,
            chunk_content=data_model.chunk_content,
            embedded_content=embedd_text(data_model.chunk_content),
            hashtags=data_model.hashtags,
            audio=data_model.audio,
            date=data_model.date,
        )

