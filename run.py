#!/usr/bin/env python
"""NovaDL - A powerful CLI downloader for video and audio from the internet.

Usage:
    python run.py                   Interactive menu
    python run.py download URL      Download video
    python run.py audio URL         Download audio only
    python run.py info URL          Show media info
    python run.py update            Update yt-dlp
    python run.py config [key] [val] View/set config
    python run.py version           Show version
    python run.py history           Show download history
    python run.py clear-history     Clear history
    python run.py doctor            System diagnosis
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from novadl.cli import main

if __name__ == "__main__":
    main()
