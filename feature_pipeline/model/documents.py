from typing import Optional, Tuple
from datetime import datetime

from models.base import VectorDBDataModel


class TikTokProfileModel(VectorDBDataModel):
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
    transcripts: str
    hashtags: str
    image: str
    audio: str
    date: datetime

    def to_payload(self) -> Tuple[str, dict]:
        data = {
            "views": self.views,
            "comments": self.comments,
            "shares": self.shares,
            "likes": self.likes,
            "bookmark": self.bookmark,
            "duration": self.duration,
            "url": self.url,
            "caption": self.caption,
            "transcripts": self.transcripts,
            "hashtags": self.hashtags,
            "image": self.image,
            "audio": self.audio,
            "date": self.date,
        }

        return self.entry_id, data