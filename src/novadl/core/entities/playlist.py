from dataclasses import dataclass, field
from typing import Optional

from novadl.core.entities.media import MediaInfo


@dataclass
class PlaylistInfo:
    title: str
    url: str
    entries: list[MediaInfo] = field(default_factory=list)
    uploader: Optional[str] = None
    uploader_url: Optional[str] = None
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    webpage_url: Optional[str] = None
    extractor: Optional[str] = None
    extractor_key: Optional[str] = None
    entry_count: int = 0
    original_json: dict = field(default_factory=dict)
