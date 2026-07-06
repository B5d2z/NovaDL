from pathlib import Path

APP_NAME = "NovaDL"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Badr Alanzi"
APP_GITHUB = "https://github.com/Badr1Alanzi/novadl"
APP_X = "@B5d2z"

CONFIG_DIR = Path.home() / ".config" / "novadl"
CONFIG_FILE = CONFIG_DIR / "config.toml"
HISTORY_FILE = CONFIG_DIR / "history.json"
LOG_FILE = CONFIG_DIR / "novadl.log"
DEFAULT_DOWNLOAD_DIR = Path.home() / "Downloads" / "NovaDL"

SUPPORTED_SITES_NOTE = (
    "All sites supported by yt-dlp, including YouTube, TikTok, Instagram, "
    "Facebook, X (Twitter), Vimeo, Reddit, Twitch, SoundCloud, and hundreds more."
)

AUDIO_EXTENSIONS = ["mp3", "m4a", "opus", "flac", "wav"]
VIDEO_EXTENSIONS = ["mp4", "mkv", "webm", "avi", "mov"]
QUALITY_OPTIONS = {
    "best": "best",
    "worst": "worst",
    "bestvideo": "bestvideo",
    "worstvideo": "worstvideo",
    "bestaudio": "bestaudio",
    "worstaudio": "worstaudio",
}

MAX_HISTORY_ENTRIES = 500
