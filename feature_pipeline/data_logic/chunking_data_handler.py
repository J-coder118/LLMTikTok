import hashlib
from abc import ABC, abstractmethod

from model.base import DataModel
from model.chunk import TikTokProfileChunkModel
from model.documents import TikTokProfileModel
from utils.chunking import chunk_text


class ChunkingDataHandler(ABC):
    """
    Abstract class for all Chunking data handlers.
    All data transformations logic for the chunking step is done here
    """

    @abstractmethod
    def chunk(self, data_model: DataModel) -> list[DataModel]:
        pass


class TikTokProfileChunkingHandler(ChunkingDataHandler):
    def chunk(self, data_model: TikTokProfileModel) -> list[TikTokProfileChunkModel]:
        data_models_list = []

        text_content = data_model.transcripts
        chunks = chunk_text(text_content)

        for chunk in chunks:
            model = TikTokProfileChunkModel(
                entry_id=data_model.entry_id,
                views=data_model.views,
                comments=data_model.comments,
                shares=data_model.shares,
                likes=data_model.likes,
                bookmark=data_model,
                duration=data_model,
                url=data_model.url,
                caption=data_model.caption,
                chunk_id=hashlib.md5(chunk.encode()).hexdigest(),
                chunk_content=chunk,
                hashtags=data_model.hashtags,
                image=data_model.image if data_model.image else None,
                audio=data_model.audio,
                date=data_model.date,
            )
            data_models_list.append(model)

        return data_models_list
