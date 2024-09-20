from typing import Optional
from model.base import DataModel
from datetime import datetime
class TikTokProfileChunkModel(DataModel):
    """
    Data model for TikTok profile chunk data
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
    hashtags: str
    image: str
    audio: str
    date: datetime