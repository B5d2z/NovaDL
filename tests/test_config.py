import json
import tempfile
from pathlib import Path

from novadl.infrastructure.config.config_manager import ConfigManager


class TestConfigManager:
    def setup_method(self) -> None:
        self.tmp = tempfile.mkdtemp()
        self.config_path = Path(self.tmp) / "config.json"
        self.manager = ConfigManager(self.config_path)

    def test_set_and_get(self) -> None:
        self.manager.set("output_dir", "/tmp/test")
        assert self.manager.get("output_dir") == "/tmp/test"

    def test_get_default(self) -> None:
        assert self.manager.get("nonexistent") is None
        assert self.manager.get("nonexistent", "default") == "default"

    def test_set_many(self) -> None:
        self.manager.set_many({"key1": "val1", "key2": "val2"})
        assert self.manager.get("key1") == "val1"
        assert self.manager.get("key2") == "val2"

    def test_get_all(self) -> None:
        self.manager.set("a", "1")
        self.manager.set("b", "2")
        all_config = self.manager.get_all()
        assert all_config == {"a": "1", "b": "2"}

    def test_delete(self) -> None:
        self.manager.set("key", "value")
        self.manager.delete("key")
        assert self.manager.get("key") is None

    def test_persistence(self) -> None:
        self.manager.set("persist", "test")
        new_manager = ConfigManager(self.config_path)
        assert new_manager.get("persist") == "test"

    def test_empty_file(self) -> None:
        self.config_path.write_text("", encoding="utf-8")
        manager = ConfigManager(self.config_path)
        assert manager.get_all() == {}

    def test_corrupted_file(self) -> None:
        self.config_path.write_text("not json", encoding="utf-8")
        manager = ConfigManager(self.config_path)
        assert manager.get_all() == {}
