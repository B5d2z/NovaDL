import shutil
import subprocess
import sys
from typing import Optional

from novadl.utils.logger import logger


class FFmpegChecker:
    @staticmethod
    def is_installed() -> bool:
        return shutil.which("ffmpeg") is not None

    @staticmethod
    def get_version() -> Optional[str]:
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                first_line = result.stdout.split("\n")[0]
                return first_line.strip()
            return None
        except FileNotFoundError:
            return None

    @staticmethod
    def get_install_guide() -> str:
        system = sys.platform
        guides = {
            "win32": """
FFmpeg is required for audio extraction and format conversion.

Installation:
1. Download from: https://ffmpeg.org/download.html
2. Extract the archive to a folder (e.g., C:\\ffmpeg)
3. Add the bin folder to your system PATH (e.g., C:\\ffmpeg\\bin)
4. Restart your terminal

Or using winget:
  winget install Gyan.FFmpeg

Or using Chocolatey:
  choco install ffmpeg
""",
            "darwin": """
FFmpeg is required for audio extraction and format conversion.

Installation using Homebrew:
  brew install ffmpeg
""",
        }

        return guides.get(
            system,
            """
FFmpeg is required for audio extraction and format conversion.

Installation:
  Ubuntu/Debian: sudo apt install ffmpeg
  Fedora: sudo dnf install ffmpeg
  Arch: sudo pacman -S ffmpeg
  Alpine: apk add ffmpeg
""",
        )
