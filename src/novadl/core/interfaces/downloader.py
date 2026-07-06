from abc import ABC, abstractmethod
from typing import Callable, Optional

from novadl.core.entities.media import DownloadResult, MediaInfo, MediaRequest
from novadl.core.entities.playlist import PlaylistInfo


class DownloaderInterface(ABC):
    @abstractmethod
    def extract_info(self, url: str, playlist: bool = False) -> MediaInfo | PlaylistInfo: ...

    @abstractmethod
    def download(
        self,
        request: MediaRequest,
        progress_callback: Optional[Callable] = None,
    ) -> DownloadResult: ...

    @abstractmethod
    def update_self(self) -> bool: ...

    @abstractmethod
    def get_version(self) -> str: ...
