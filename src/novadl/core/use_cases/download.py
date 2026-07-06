from pathlib import Path
from typing import Callable, Optional

from novadl.core.entities.media import (
    DownloadResult,
    MediaRequest,
    MediaType,
)
from novadl.core.interfaces.downloader import DownloaderInterface
from novadl.core.interfaces.repository import (
    ConfigRepositoryInterface,
    HistoryRepositoryInterface,
)
from novadl.utils.exceptions import DownloadError
from novadl.utils.logger import logger


class DownloadUseCase:
    def __init__(
        self,
        downloader: DownloaderInterface,
        config: ConfigRepositoryInterface,
        history: HistoryRepositoryInterface,
    ) -> None:
        self._downloader = downloader
        self._config = config
        self._history = history

    def execute_single(
        self,
        url: str,
        output_dir: Optional[Path] = None,
        quality: Optional[str] = None,
        audio_only: bool = False,
        audio_format: str = "mp3",
        audio_quality: str = "192",
        output_format: Optional[str] = None,
        subtitles: bool = False,
        subtitle_langs: Optional[list[str]] = None,
        embed_subs: bool = False,
        write_thumbnail: bool = False,
        cookies_file: Optional[Path] = None,
        proxy_url: Optional[str] = None,
        progress_callback: Optional[Callable] = None,
    ) -> DownloadResult:
        if output_dir is None:
            output_dir_str = self._config.get("output_dir")
            output_dir = Path(output_dir_str) if output_dir_str else Path.home() / "Downloads" / "NovaDL"
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

        request = MediaRequest(
            url=url,
            output_dir=output_dir,
            audio_only=audio_only,
            audio_format=audio_format,
            audio_quality=audio_quality,
            output_format=output_format,
            subtitles=subtitles,
            subtitle_langs=subtitle_langs,
            embed_subs=embed_subs,
            write_thumbnail=write_thumbnail,
            cookies_file=cookies_file,
            proxy_url=proxy_url,
            filename_template="%(title)s.%(ext)s",
        )

        try:
            logger.info("Starting download: %s", url)
            result = self._downloader.download(request, progress_callback)
            if result.success:
                self._history.add_entry(result)
                logger.info("Download completed: %s -> %s", url, result.file_path)
            else:
                logger.error("Download failed: %s - %s", url, result.error_message)
            return result
        except Exception as e:
            logger.exception("Download error for %s", url)
            raise DownloadError(str(e)) from e

    def execute_info(self, url: str) -> dict:
        try:
            logger.info("Extracting info for: %s", url)
            info = self._downloader.extract_info(url)
            return info.original_json if hasattr(info, "original_json") else {}
        except Exception as e:
            logger.exception("Info extraction failed for %s", url)
            raise DownloadError(str(e)) from e
