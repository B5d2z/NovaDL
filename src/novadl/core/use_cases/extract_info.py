from novadl.core.entities.media import MediaInfo
from novadl.core.entities.playlist import PlaylistInfo
from novadl.core.interfaces.downloader import DownloaderInterface
from novadl.utils.exceptions import ExtractionError
from novadl.utils.logger import logger


class ExtractInfoUseCase:
    def __init__(self, downloader: DownloaderInterface) -> None:
        self._downloader = downloader

    def execute(self, url: str) -> MediaInfo | PlaylistInfo:
        try:
            logger.info("Extracting info for: %s", url)
            info = self._downloader.extract_info(url)

            if isinstance(info, PlaylistInfo) and info.entry_count == 1 and info.entries:
                return info.entries[0]

            return info
        except Exception as e:
            logger.exception("Info extraction failed for %s", url)
            raise ExtractionError(str(e)) from e
