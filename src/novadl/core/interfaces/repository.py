from abc import ABC, abstractmethod
from typing import Optional

from novadl.core.entities.media import DownloadResult


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
