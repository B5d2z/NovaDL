import json
from pathlib import Path
from typing import Optional

from novadl.core.entities.media import DownloadResult, MediaType
from novadl.core.interfaces.repository import HistoryRepositoryInterface
from novadl.utils.constants import CONFIG_DIR, HISTORY_FILE, MAX_HISTORY_ENTRIES
from novadl.utils.logger import logger


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
                content = self._history_file.read_text(encoding="utf-8")
                if content.strip():
                    raw: list[dict] = json.loads(content)
                    self._entries = [self._dict_to_result(d) for d in raw]
                else:
                    self._entries = []
            else:
                self._entries = []
        except (json.JSONDecodeError, OSError) as e:
            logger.error("Failed to load history: %s", e)
            self._entries = []

    def _save(self) -> None:
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            raw = [self._result_to_dict(r) for r in self._entries]
            self._history_file.write_text(
                json.dumps(raw, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except OSError as e:
            logger.error("Failed to save history: %s", e)

    def _result_to_dict(self, r: DownloadResult) -> dict:
        return {
            "url": r.url,
            "title": r.title,
            "file_path": str(r.file_path),
            "media_type": r.media_type.value,
            "file_size": r.file_size,
            "duration": r.duration,
            "success": r.success,
            "error_message": r.error_message,
        }

    def _dict_to_result(self, d: dict) -> DownloadResult:
        return DownloadResult(
            url=d.get("url", ""),
            title=d.get("title", "Unknown"),
            file_path=Path(d.get("file_path", "")),
            media_type=MediaType(d.get("media_type", "video")),
            file_size=d.get("file_size", 0),
            duration=d.get("duration"),
            success=d.get("success", True),
            error_message=d.get("error_message", ""),
        )
