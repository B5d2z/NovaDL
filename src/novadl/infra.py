import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Optional

import yt_dlp

from novadl.const import CONFIG_DIR, CONFIG_FILE, ExtractionError, HISTORY_FILE, MAX_HISTORY_ENTRIES, logger
from novadl.core import (
    ConfigRepositoryInterface,
    DownloadResult,
    DownloaderInterface,
    HistoryRepositoryInterface,
    MediaInfo,
    MediaRequest,
    MediaType,
    PlaylistInfo,
)
from novadl.const import ExtractionError


class YtDlpDownloader(DownloaderInterface):
    def extract_info(self, url: str, playlist: bool = False) -> MediaInfo | PlaylistInfo:
        opts: dict[str, Any] = {"quiet": True, "no_warnings": True, "extract_flat": False}
        if not playlist:
            opts["playlist_items"] = "1"
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                raw = ydl.extract_info(url, download=False)
            if raw is None:
                raise ExtractionError("No data returned")
            return self._parse(raw, url)
        except yt_dlp.utils.DownloadError as e:
            raise ExtractionError(str(e)) from e

    def download(self, request: MediaRequest, progress_callback: Optional[Callable] = None) -> DownloadResult:
        opts: dict[str, Any] = {
            "outtmpl": str(request.output_dir / request.filename_template) if request.output_dir else request.filename_template,
            "quiet": True, "no_warnings": True, "continuedl": request.resume,
        }
        if request.audio_only:
            opts["format"] = "bestaudio/best"
            opts["postprocessors"] = [{"key": "FFmpegExtractAudio", "preferredcodec": request.audio_format, "preferredquality": request.audio_quality}]
        else:
            opts["format"] = request.quality
        if request.cookies_file and request.cookies_file.exists():
            opts["cookiefile"] = str(request.cookies_file)
        if request.proxy_url:
            opts["proxy"] = request.proxy_url
        if request.subtitles:
            opts["writesubtitles"] = True
            opts["writeautomaticsub"] = True
            opts["subtitleslangs"] = request.subtitle_langs or ["en"]
            if request.embed_subs:
                opts.setdefault("postprocessors", []).append({"key": "FFmpegEmbedSubtitle"})
        if request.write_thumbnail:
            opts["writethumbnail"] = True
        if progress_callback:
            opts["progress_hooks"] = [progress_callback]

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                raw = ydl.extract_info(request.url, download=True)
            file_path = request.output_dir / f"{yt_dlp.utils.sanitize_filename(raw.get('title', 'Unknown'))}." + (request.audio_format if request.audio_only else "mp4") if request.output_dir else Path(f"{raw.get('title', 'Unknown')}.mp4")
            return DownloadResult(url=request.url, title=raw.get("title", "Unknown"), file_path=file_path, media_type=request.media_type, file_size=file_path.stat().st_size if file_path.exists() else 0, duration=raw.get("duration"))
        except yt_dlp.utils.DownloadError as e:
            return DownloadResult(url=request.url, title="Unknown", file_path=Path(), media_type=request.media_type, file_size=0, success=False, error_message=str(e))

    def update_self(self) -> bool:
        try:
            r = subprocess.run([sys.executable, "-m", "yt_dlp", "--update"], capture_output=True, text=True, check=False)
            return r.returncode == 0
        except Exception:
            return False

    def get_version(self) -> str:
        try:
            r = subprocess.run([sys.executable, "-m", "yt_dlp", "--version"], capture_output=True, text=True, check=False)
            return r.stdout.strip() or "unknown"
        except Exception:
            return "unknown"

    def _parse(self, raw: dict[str, Any], url: str) -> MediaInfo | PlaylistInfo:
        if raw.get("_type") == "playlist" or "entries" in raw:
            entries = [self._build_info(e, e.get("webpage_url", url)) for e in (raw.get("entries") or []) if e]
            return PlaylistInfo(title=raw.get("title", "Untitled"), url=url, entries=entries, uploader=raw.get("uploader"), entry_count=len(entries), webpage_url=raw.get("webpage_url", url), extractor=raw.get("extractor"), original_json=raw)
        return self._build_info(raw, url)

    def _build_info(self, raw: dict[str, Any], url: str) -> MediaInfo:
        return MediaInfo(url=url, title=raw.get("title", "Unknown"), media_type=MediaType.VIDEO, duration=raw.get("duration"), uploader=raw.get("uploader"), upload_date=raw.get("upload_date"), description=raw.get("description"), thumbnail=raw.get("thumbnail"), webpage_url=raw.get("webpage_url", url), extractor=raw.get("extractor"), formats=raw.get("formats", []), subtitles=raw.get("subtitles", {}), original_json=raw)


class ConfigManager(ConfigRepositoryInterface):
    def __init__(self, config_file: Path = CONFIG_FILE) -> None:
        self._config_file = config_file
        self._data: dict[str, str] = {}
        self.load()

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return self._data.get(key, default)
    def set(self, key: str, value: str) -> None:
        self._data[key] = value
        self.save()
    def set_many(self, pairs: dict[str, str]) -> None:
        self._data.update(pairs)
        self.save()
    def get_all(self) -> dict[str, str]:
        return dict(self._data)
    def delete(self, key: str) -> None:
        self._data.pop(key, None)
        self.save()
    def load(self) -> None:
        try:
            if self._config_file.exists():
                c = self._config_file.read_text(encoding="utf-8")
                self._data = json.loads(c) if c.strip() else {}
            else:
                self._data = {}
        except (json.JSONDecodeError, OSError):
            self._data = {}
    def save(self) -> None:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self._config_file.write_text(json.dumps(self._data, indent=2, ensure_ascii=False), encoding="utf-8")


class HistoryManager(HistoryRepositoryInterface):
    def __init__(self, history_file: Path = HISTORY_FILE) -> None:
        self._history_file = history_file
        self._entries: list[DownloadResult] = []
        self._load()

    def add_entry(self, entry: DownloadResult) -> None:
        self._entries.insert(0, entry)
        if len(self._entries) > MAX_HISTORY_ENTRIES:
            self._entries = self._entries[:MAX_HISTORY_ENTRIES]
        self._save()
    def get_all(self) -> list[DownloadResult]:
        return list(self._entries)
    def clear(self) -> None:
        self._entries.clear()
        self._save()
    def get_last(self, n: int) -> list[DownloadResult]:
        return self._entries[:n]

    def _load(self) -> None:
        try:
            if self._history_file.exists():
                c = self._history_file.read_text(encoding="utf-8")
                self._entries = [self._dict_to_result(d) for d in (json.loads(c) if c.strip() else [])] if c.strip() else []
            else:
                self._entries = []
        except (json.JSONDecodeError, OSError):
            self._entries = []

    def _save(self) -> None:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self._history_file.write_text(json.dumps([self._result_to_dict(r) for r in self._entries], indent=2, ensure_ascii=False), encoding="utf-8")

    def _result_to_dict(self, r: DownloadResult) -> dict:
        return {"url": r.url, "title": r.title, "file_path": str(r.file_path), "media_type": r.media_type.value, "file_size": r.file_size, "duration": r.duration, "success": r.success, "error_message": r.error_message}
    def _dict_to_result(self, d: dict) -> DownloadResult:
        return DownloadResult(url=d.get("url", ""), title=d.get("title", "Unknown"), file_path=Path(d.get("file_path", "")), media_type=MediaType(d.get("media_type", "video")), file_size=d.get("file_size", 0), duration=d.get("duration"), success=d.get("success", True), error_message=d.get("error_message", ""))


class FFmpegChecker:
    @staticmethod
    def is_installed() -> bool:
        return shutil.which("ffmpeg") is not None

    @staticmethod
    def get_version() -> Optional[str]:
        try:
            r = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, check=False)
            return r.stdout.split("\n")[0].strip() if r.returncode == 0 else None
        except FileNotFoundError:
            return None

    @staticmethod
    def get_install_guide() -> str:
        guides = {
            "win32": "\nInstall FFmpeg:\n1. Download from: https://ffmpeg.org/download.html\n2. Extract to C:\\ffmpeg\n3. Add C:\\ffmpeg\\bin to PATH\n4. Restart terminal\n",
            "darwin": "\nInstall FFmpeg:\n  brew install ffmpeg\n",
        }
        return guides.get(sys.platform, "\nInstall FFmpeg:\n  Ubuntu/Debian: sudo apt install ffmpeg\n  Fedora: sudo dnf install ffmpeg\n  Arch: sudo pacman -S ffmpeg\n")
