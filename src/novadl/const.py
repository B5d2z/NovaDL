import logging
import sys
from pathlib import Path
from typing import Optional

APP_NAME = "NovaDL"
APP_VERSION = "1.0.0"
APP_AUTHOR = "B5t Alanzi"
APP_GITHUB = "https://github.com/Badr1Alanzi/novadl"
APP_X = "@B5d2z"

CONFIG_DIR = Path.home() / ".config" / "novadl"
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE = CONFIG_DIR / "history.json"
LOG_FILE = CONFIG_DIR / "novadl.log"
DEFAULT_DOWNLOAD_DIR = Path.home() / "Videos" / "NovaDL"

AUDIO_EXTENSIONS = ["mp3", "m4a", "opus", "flac", "wav"]
VIDEO_EXTENSIONS = ["mp4", "mkv", "webm", "avi", "mov"]
MAX_HISTORY_ENTRIES = 500


class NovaDLError(Exception):
    """Base exception for all NovaDL errors."""


class DownloadError(NovaDLError):
    """Raised when a download fails."""


class ExtractionError(NovaDLError):
    """Raised when information extraction fails."""


class ConfigurationError(NovaDLError):
    """Raised when configuration loading or saving fails."""


class FFmpegNotFoundError(NovaDLError):
    """Raised when FFmpeg is required but not found."""


class InvalidURLError(NovaDLError):
    """Raised when a provided URL is invalid or unsupported."""


def setup_logger(name: str = "novadl") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    ch = logging.StreamHandler(sys.stderr)
    ch.setLevel(logging.WARNING)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


logger = setup_logger()
