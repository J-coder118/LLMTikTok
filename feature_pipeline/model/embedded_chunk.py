from typing import Tuple
import numpy as np

from models.base import VectorDBDataModel

class TikTokProfileEmbeddedChunkModel(VectorDBDataModel):
    """
    Data model for TikTok profile data
    """
    entry_id: int
    views: int
    comments: int
    shares: int
    likes: int
    bookmark: int
    duration: int
    url: str
    caption: str
    chunk_id: str
    chunk_content: str
    embedded_content: np.ndarray
    hashtags: str
    audio: str
    date: datetime

    class Config:
        arbitrary_types_allowed = True

    def to_payload(self) -> Tuple[str, np.ndarray dict]:
        data = {
            "views": self.views,
            "comments": self.comments,
            "shares": self.shares,
            "likes": self.likes,
            "bookmark": self.bookmark,
            "duration": self.duration,
            "url": self.url,
            "caption": self.caption,
            "transcripts": self.chunk_content,
            "hashtags": self.hashtags,
            "audio": self.audio,
            "date": self.date,
        }

        return self.chunk_id, self.embedded_content, data