import json
from pathlib import Path
from typing import Optional

from novadl.core.interfaces.repository import ConfigRepositoryInterface
from novadl.utils.constants import CONFIG_DIR, CONFIG_FILE
from novadl.utils.exceptions import ConfigurationError
from novadl.utils.logger import logger


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
                content = self._config_file.read_text(encoding="utf-8")
                if content.strip():
                    self._data = json.loads(content)
                else:
                    self._data = {}
            else:
                self._data = {}
        except (json.JSONDecodeError, OSError) as e:
            logger.error("Failed to load config: %s", e)
            self._data = {}

    def save(self) -> None:
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            self._config_file.write_text(
                json.dumps(self._data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except OSError as e:
            raise ConfigurationError(f"Failed to save config: {e}") from e
