from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable, Optional

from novadl.const import DEFAULT_DOWNLOAD_DIR, DownloadError, logger


class MediaType(Enum):
    VIDEO = "video"
    AUDIO = "audio"
    PLAYLIST = "playlist"


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
class PlaylistInfo:
    title: str
    url: str
    entries: list[MediaInfo] = field(default_factory=list)
    uploader: Optional[str] = None
    uploader_url: Optional[str] = None
    entry_count: int = 0
    webpage_url: Optional[str] = None
    extractor: Optional[str] = None
    original_json: dict = field(default_factory=dict)


@dataclass
class MediaRequest:
    url: str
    media_type: MediaType = MediaType.VIDEO
    quality: str = "best"
    output_dir: Optional[Path] = None
    filename_template: str = "%(title)s.%(ext)s"
    extract_audio: bool = False
    audio_only: bool = False
    audio_format: str = "mp3"
    audio_quality: str = "192"
    subtitles: bool = False
    subtitle_langs: Optional[list[str]] = None
    embed_subs: bool = False
    write_thumbnail: bool = False
    cookies_file: Optional[Path] = None
    proxy_url: Optional[str] = None
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


class DownloaderInterface(ABC):
    @abstractmethod
    def extract_info(self, url: str, playlist: bool = False) -> MediaInfo | PlaylistInfo: ...

    @abstractmethod
    def download(self, request: MediaRequest, progress_callback: Optional[Callable] = None) -> DownloadResult: ...

    @abstractmethod
    def update_self(self) -> bool: ...

    @abstractmethod
    def get_version(self) -> str: ...


class HistoryRepositoryInterface(ABC):
    @abstractmethod
    def add_entry(self, entry: DownloadResult) -> None: ...
    @abstractmethod
    def get_all(self) -> list[DownloadResult]: ...
    @abstractmethod
    def clear(self) -> None: ...
    @abstractmethod
    def get_last(self, n: int) -> list[DownloadResult]: ...


class ConfigRepositoryInterface(ABC):
    @abstractmethod
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]: ...
    @abstractmethod
    def set(self, key: str, value: str) -> None: ...
    @abstractmethod
    def set_many(self, pairs: dict[str, str]) -> None: ...
    @abstractmethod
    def get_all(self) -> dict[str, str]: ...
    @abstractmethod
    def delete(self, key: str) -> None: ...
    @abstractmethod
    def load(self) -> None: ...
    @abstractmethod
    def save(self) -> None: ...


class DownloadUseCase:
    def __init__(self, downloader: DownloaderInterface, config: ConfigRepositoryInterface, history: HistoryRepositoryInterface) -> None:
        self._downloader = downloader
        self._config = config
        self._history = history

    def execute_single(self, url: str, output_dir: Optional[Path] = None, quality: Optional[str] = None, audio_only: bool = False, audio_format: str = "mp3", audio_quality: str = "192", output_format: Optional[str] = None, subtitles: bool = False, subtitle_langs: Optional[list[str]] = None, embed_subs: bool = False, write_thumbnail: bool = False, cookies_file: Optional[Path] = None, proxy_url: Optional[str] = None, progress_callback: Optional[Callable] = None) -> DownloadResult:
        if output_dir is None:
            od = self._config.get("output_dir")
            output_dir = Path(od) if od else DEFAULT_DOWNLOAD_DIR
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

        request = MediaRequest(url=url, output_dir=output_dir, audio_only=audio_only, audio_format=audio_format, audio_quality=audio_quality, subtitles=subtitles, subtitle_langs=subtitle_langs, embed_subs=embed_subs, write_thumbnail=write_thumbnail, cookies_file=cookies_file, proxy_url=proxy_url)
        try:
            logger.info("Starting download: %s", url)
            result = self._downloader.download(request, progress_callback)
            if result.success:
                self._history.add_entry(result)
            return result
        except Exception as e:
            raise DownloadError(str(e)) from e


class ExtractInfoUseCase:
    def __init__(self, downloader: DownloaderInterface) -> None:
        self._downloader = downloader

    def execute(self, url: str) -> MediaInfo | PlaylistInfo:
        return self._downloader.extract_info(url)


class UpdateUseCase:
    def __init__(self, downloader: DownloaderInterface) -> None:
        self._downloader = downloader

    def execute(self) -> bool:
        return self._downloader.update_self()



