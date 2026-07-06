from novadl.core.interfaces.downloader import DownloaderInterface
from novadl.utils.exceptions import UpdateError
from novadl.utils.logger import logger


class UpdateUseCase:
    def __init__(self, downloader: DownloaderInterface) -> None:
        self._downloader = downloader

    def execute(self) -> bool:
        try:
            logger.info("Attempting to update yt-dlp")
            result = self._downloader.update_self()
            if result:
                logger.info("yt-dlp updated successfully")
            else:
                logger.info("yt-dlp is already up to date")
            return result
        except Exception as e:
            logger.exception("Update failed")
            raise UpdateError(str(e)) from e
