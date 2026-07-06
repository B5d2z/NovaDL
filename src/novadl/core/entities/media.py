from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional


class MediaType(Enum):
    VIDEO = "video"
    AUDIO = "audio"
    PLAYLIST = "playlist"


class MediaQuality(Enum):
    BEST = "best"
    WORST = "worst"
    BEST_VIDEO = "bestvideo"
    WORST_VIDEO = "worstvideo"
    BEST_AUDIO = "bestaudio"
    WORST_AUDIO = "worstaudio"


@dataclass
class MediaInfo:
    url: str
    title: str
    media_type: MediaType
    duration: Optional[int] = None
    uploader: Optional[str] = None
    upload_date: Optional[str] = None
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    webpage_url: Optional[str] = None
    extractor: Optional[str] = None
    extractor_key: Optional[str] = None
    formats: list[dict] = field(default_factory=list)
    subtitles: dict = field(default_factory=dict)
    automatic_captions: dict = field(default_factory=dict)
    original_json: dict = field(default_factory=dict)

    @property
    def duration_str(self) -> str:
        if self.duration is None:
            return "N/A"
        minutes, seconds = divmod(self.duration, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        return f"{minutes}:{seconds:02d}"


@dataclass
class MediaRequest:
    url: str
    media_type: MediaType = MediaType.VIDEO
    quality: MediaQuality = MediaQuality.BEST
    format_id: Optional[str] = None
    output_format: Optional[str] = None
    output_dir: Optional[Path] = None
    filename_template: str = "%(title)s.%(ext)s"
    extract_audio: bool = False
    audio_only: bool = False
    audio_format: str = "mp3"
    audio_quality: str = "192"
    subtitles: bool = False
    subtitle_langs: Optional[list[str]] = None
    embed_subs: bool = False
    embed_thumbnail: bool = False
    write_thumbnail: bool = False
    write_metadata: bool = False
    cookies_file: Optional[Path] = None
    proxy_url: Optional[str] = None
    limit_rate: Optional[str] = None
    resume: bool = True


@dataclass
class DownloadResult:
    url: str
    title: str
    file_path: Path
    media_type: MediaType
    file_size: int
    duration: Optional[int] = None
    success: bool = True
    error_message: str = ""
