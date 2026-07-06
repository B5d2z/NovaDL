import tempfile
from pathlib import Path

from novadl.core.entities.media import DownloadResult, MediaType
from novadl.infrastructure.history.history_manager import HistoryManager


class TestHistoryManager:
    def setup_method(self) -> None:
        self.tmp = tempfile.mkdtemp()
        self.history_path = Path(self.tmp) / "history.json"
        self.manager = HistoryManager(self.history_path)

    def _make_entry(self, title: str = "Test Video") -> DownloadResult:
        return DownloadResult(
            url="https://example.com/video",
            title=title,
            file_path=Path("/tmp/test.mp4"),
            media_type=MediaType.VIDEO,
            file_size=1024,
            duration=120,
        )

    def test_add_and_get_all(self) -> None:
        entry = self._make_entry()
        self.manager.add_entry(entry)
        entries = self.manager.get_all()
        assert len(entries) == 1
        assert entries[0].title == "Test Video"

    def test_clear(self) -> None:
        self.manager.add_entry(self._make_entry())
        self.manager.clear()
        assert len(self.manager.get_all()) == 0

    def test_get_last(self) -> None:
        for i in range(5):
            self.manager.add_entry(self._make_entry(f"Video {i}"))
        last = self.manager.get_last(2)
        assert len(last) == 2

    def test_persistence(self) -> None:
        self.manager.add_entry(self._make_entry("Persist Test"))
        new_manager = HistoryManager(self.history_path)
        entries = new_manager.get_all()
        assert len(entries) == 1
        assert entries[0].title == "Persist Test"

    def test_max_entries(self) -> None:
        from novadl.utils.constants import MAX_HISTORY_ENTRIES

        for i in range(MAX_HISTORY_ENTRIES + 10):
            self.manager.add_entry(self._make_entry(f"Video {i}"))
        assert len(self.manager.get_all()) == MAX_HISTORY_ENTRIES
