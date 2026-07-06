import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Optional

import yt_dlp

from novadl.core.entities.media import (
    DownloadResult,
    MediaInfo,
    MediaRequest,
    MediaType,
)
from novadl.core.entities.playlist import PlaylistInfo
from novadl.core.interfaces.downloader import DownloaderInterface
from novadl.utils.exceptions import DownloadError, ExtractionError
from novadl.utils.logger import logger


class YtDlpDownloader(DownloaderInterface):
    def extract_info(self, url: str, playlist: bool = False) -> MediaInfo | PlaylistInfo:
        opts: dict[str, Any] = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
        }

        if not playlist:
            opts["playlist_items"] = "1"

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                raw = ydl.extract_info(url, download=False)

            if raw is None:
                raise ExtractionError("Failed to extract info: no data returned")

            return self._parse_extracted_info(raw, url)
        except yt_dlp.utils.DownloadError as e:
            raise ExtractionError(str(e)) from e

    def download(
        self,
        request: MediaRequest,
        progress_callback: Optional[Callable] = None,
    ) -> DownloadResult:
        opts = self._build_opts(request, progress_callback)

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                raw = ydl.extract_info(request.url, download=True)

            if raw is None:
                raise DownloadError("Download completed but no data returned")

            file_path = self._get_output_path(raw, request)
            file_size = self._get_file_size(file_path)

            return DownloadResult(
                url=request.url,
                title=raw.get("title", "Unknown"),
                file_path=file_path,
                media_type=request.media_type,
                file_size=file_size,
                duration=raw.get("duration"),
            )
        except yt_dlp.utils.DownloadError as e:
            return DownloadResult(
                url=request.url,
                title="Unknown",
                file_path=Path(),
                media_type=request.media_type,
                file_size=0,
                success=False,
                error_message=str(e),
            )

    def update_self(self) -> bool:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "yt_dlp", "--update"],
                capture_output=True,
                text=True,
                check=False,
            )
            return result.returncode == 0
        except Exception as e:
            logger.error("Failed to update yt-dlp: %s", e)
            return False

    def get_version(self) -> str:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "yt_dlp", "--version"],
                capture_output=True,
                text=True,
                check=False,
            )
            return result.stdout.strip() or "unknown"
        except Exception:
            return "unknown"

    def _build_opts(
        self,
        request: MediaRequest,
        progress_callback: Optional[Callable] = None,
    ) -> dict[str, Any]:
        outtmpl = str(request.output_dir / request.filename_template) if request.output_dir else request.filename_template

        opts: dict[str, Any] = {
            "outtmpl": outtmpl,
            "quiet": True,
            "no_warnings": True,
            "continuedl": request.resume,
        }

        if request.audio_only:
            opts["format"] = "bestaudio/best"
            opts["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": request.audio_format,
                    "preferredquality": request.audio_quality,
                }
            ]
        elif request.format_id:
            opts["format"] = request.format_id
        else:
            opts["format"] = request.quality.value

        if request.output_format:
            opts["merge_output_format"] = request.output_format

        if request.cookies_file and request.cookies_file.exists():
            opts["cookiefile"] = str(request.cookies_file)

        if request.proxy_url:
            opts["proxy"] = request.proxy_url

        if request.limit_rate:
            opts["ratelimit"] = request.limit_rate

        if request.subtitles:
            opts["writesubtitles"] = True
            opts["writeautomaticsub"] = True
            if request.subtitle_langs:
                opts["subtitleslangs"] = request.subtitle_langs
            else:
                opts["subtitleslangs"] = ["en"]
            if request.embed_subs:
                opts["postprocessors"] = opts.get("postprocessors", []) + [
                    {"key": "FFmpegEmbedSubtitle"}
                ]

        if request.write_thumbnail:
            opts["writethumbnail"] = True
            if request.embed_thumbnail:
                pp = opts.setdefault("postprocessors", [])
                pp.append({"key": "EmbedThumbnail"})

        if request.write_metadata:
            opts["writeinfojson"] = True

        if progress_callback:
            opts["progress_hooks"] = [progress_callback]

        return opts

    def _parse_extracted_info(
        self,
        raw: dict[str, Any],
        url: str,
    ) -> MediaInfo | PlaylistInfo:
        if raw.get("_type") == "playlist" or "entries" in raw:
            entries = raw.get("entries") or []
            playlist_entries = []
            for entry in entries:
                if entry is None:
                    continue
                playlist_entries.append(self._build_media_info(entry, entry.get("webpage_url", url)))

            return PlaylistInfo(
                title=raw.get("title", "Untitled Playlist"),
                url=url,
                entries=playlist_entries,
                uploader=raw.get("uploader"),
                uploader_url=raw.get("uploader_url"),
                description=raw.get("description"),
                thumbnail=raw.get("thumbnail"),
                webpage_url=raw.get("webpage_url", url),
                extractor=raw.get("extractor"),
                extractor_key=raw.get("extractor_key"),
                entry_count=len(playlist_entries),
                original_json=raw,
            )

        return self._build_media_info(raw, url)

    def _build_media_info(self, raw: dict[str, Any], url: str) -> MediaInfo:
        return MediaInfo(
            url=url,
            title=raw.get("title", "Unknown"),
            media_type=MediaType.VIDEO,
            duration=raw.get("duration"),
            uploader=raw.get("uploader"),
            upload_date=raw.get("upload_date"),
            description=raw.get("description"),
            thumbnail=raw.get("thumbnail"),
            webpage_url=raw.get("webpage_url", url),
            extractor=raw.get("extractor"),
            extractor_key=raw.get("extractor_key"),
            formats=raw.get("formats", []),
            subtitles=raw.get("subtitles", {}),
            automatic_captions=raw.get("automatic_captions", {}),
            original_json=raw,
        )

    def _get_output_path(self, raw: dict[str, Any], request: MediaRequest) -> Path:
        filename = yt_dlp.utils.sanitize_filename(raw.get("title", "Unknown"))
        ext = request.output_format or "mp4"
        if request.output_dir:
            return request.output_dir / f"{filename}.{ext}"
        return Path(f"{filename}.{ext}")

    def _get_file_size(self, file_path: Path) -> int:
        try:
            return file_path.stat().st_size if file_path.exists() else 0
        except OSError:
            return 0
