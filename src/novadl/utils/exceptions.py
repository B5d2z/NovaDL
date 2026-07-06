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


class UpdateError(NovaDLError):
    """Raised when yt-dlp update fails."""


class QueueError(NovaDLError):
    """Raised when a queue operation fails."""
