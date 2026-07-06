# NovaDL

A powerful, professional CLI downloader for video and audio from YouTube, TikTok, Instagram, Facebook, X (Twitter), Vimeo, Reddit, Twitch, SoundCloud, and hundreds of other websites.

Built on top of [yt-dlp](https://github.com/yt-dlp/yt-dlp) with a clean architecture, rich terminal interface, and production-grade code quality.

## Features

- **Video Downloading** — Download videos from any site yt-dlp supports
- **Audio Extraction** — Extract audio in MP3, M4A, Opus, FLAC, or WAV
- **Quality Selection** — Choose video and audio quality (best, worst, custom)
- **Format Selection** — Choose output format (mp4, mkv, webm, etc.)
- **Playlist Support** — Download entire playlists and channels
- **Subtitle Support** — Download and embed subtitles
- **Thumbnail Support** — Download and embed thumbnails
- **Metadata Extraction** — View detailed media information and metadata
- **Resume Support** — Resume interrupted downloads
- **Batch Downloads** — Process multiple URLs from a file
- **Cookie Support** — Use cookies for authenticated downloads
- **Proxy Support** — Route downloads through a proxy
- **Configuration** — Persistent settings via config file
- **Download History** — Track and review past downloads
- **yt-dlp Update** — Update yt-dlp directly from the CLI
- **FFmpeg Detection** — Check for FFmpeg and get installation guidance
- **Rich Terminal UI** — Progress bars, speed indicators, time remaining, and clean output

## Installation

### Prerequisites

- Python 3.12 or later
- [FFmpeg](https://ffmpeg.org/) (required for audio extraction and format conversion)

### Install via pip

```bash
pip install novadl
```

### Install via Poetry

```bash
git clone https://github.com/Badr1Alanzi/novadl.git
cd novadl
poetry install
```

### Install via pip (development)

```bash
git clone https://github.com/Badr1Alanzi/novadl.git
cd novadl
pip install -e .
```

## Usage

### Download a video

```bash
novadl download "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Download audio only

```bash
novadl audio "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Choose quality and format

```bash
novadl download "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --quality best --format mp4
```

### Download with subtitles

```bash
novadl download "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --subtitles --sub-langs en,ar --embed-subs
```

### Custom output directory

```bash
novadl download "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --output-dir ~/Videos/NovaDL
```

### Using a proxy

```bash
novadl download "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --proxy "http://127.0.0.1:8080"
```

### Using cookies

```bash
novadl download "https://www.example.com/video" --cookies /path/to/cookies.txt
```

### Get media information

```bash
novadl info "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

## Commands

| Command | Description |
|---------|-------------|
| `novadl download <url>` | Download a video with optional quality, format, and subtitle options |
| `novadl audio <url>` | Download audio only (MP3, M4A, Opus, FLAC, WAV) |
| `novadl info <url>` | Display detailed information about a media URL |
| `novadl update` | Update yt-dlp to the latest version |
| `novadl config [key] [value]` | View or modify configuration settings |
| `novadl version` | Display version information |
| `novadl history` | View download history |
| `novadl clear-history` | Clear all download history |
| `novadl doctor` | Run system diagnostics (yt-dlp, FFmpeg) |

### Download Options

| Option | Short | Description |
|--------|-------|-------------|
| `--output-dir` | `-o` | Output directory for downloads |
| `--quality` | `-q` | Video quality (best, worst, bestvideo, worstvideo) |
| `--format` | `-f` | Output format/extension (mp4, mkv, webm, etc.) |
| `--audio-only` | `-a` | Download audio only |
| `--audio-format` | | Audio format (mp3, m4a, opus, flac, wav) |
| `--audio-quality` | | Audio quality in kbps |
| `--subtitles` | `-s` | Download subtitles |
| `--sub-langs` | | Subtitle language codes (comma separated) |
| `--embed-subs` | | Embed subtitles into video |
| `--thumbnail` | `-t` | Write thumbnail |
| `--cookies` | `-c` | Path to cookies file |
| `--proxy` | `-p` | Proxy URL |

## Supported Platforms

- Windows 10 / 11
- macOS 12+
- Linux (any distribution with Python 3.12+)

## Supported Sites

All websites supported by yt-dlp, including:

YouTube, YouTube Music, YouTube Shorts, TikTok, Instagram, Facebook, X (Twitter), Vimeo, Reddit, Twitch, SoundCloud, Dailymotion, Bilibili, Niconico, PornHub, XVideos, and hundreds more.

See the [yt-dlp supported sites list](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) for a complete list.

## Configuration

NovaDL stores its configuration in `~/.config/novadl/config.toml`.

### View all settings

```bash
novadl config
```

### View a specific setting

```bash
novadl config output_dir
```

### Set a value

```bash
novadl config output_dir "~/Videos/NovaDL"
```

### Available Configuration Keys

| Key | Description | Default |
|-----|-------------|---------|
| `output_dir` | Default download directory | `~/Downloads/NovaDL` |
| `proxy` | Default proxy URL | — |
| `cookies` | Default cookies file path | — |
| `audio_format` | Default audio format | `mp3` |
| `audio_quality` | Default audio quality (kbps) | `192` |

## FAQ

**Q: Do I need FFmpeg?**

A: FFmpeg is required for audio extraction and format conversion. If you're only downloading video in its original format, FFmpeg is optional.

**Q: How do I install FFmpeg?**

A: Run `novadl doctor` for platform-specific installation instructions.

**Q: Can I use this on Windows?**

A: Yes. NovaDL is fully supported on Windows, macOS, and Linux.

**Q: Can I download private YouTube videos?**

A: Yes, if you provide authentication via a cookies file using the `--cookies` option.

**Q: How do I update yt-dlp?**

A: Run `novadl update` to update yt-dlp to the latest version.

## Project Structure

```
src/novadl/
├── cli/              # Typer CLI commands and interface
├── core/             # Domain logic (entities, use cases, interfaces)
│   ├── entities/     # Data models
│   ├── use_cases/    # Business logic
│   └── interfaces/   # Abstract interfaces
├── infrastructure/   # External integrations
│   ├── downloader/   # yt-dlp integration
│   ├── config/       # Configuration management
│   ├── history/      # Download history
│   └── system/       # System utilities
├── presentation/     # Rich terminal output
└── utils/            # Shared utilities
```

## Development

```bash
# Install dependencies
poetry install

# Run linting
poetry run ruff check src/

# Run formatting
poetry run black src/ tests/

# Run type checking
poetry run mypy src/

# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=src/novadl --cov-report=html
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Author

**Badr Alanzi**

- GitHub: [@Badr1Alanzi](https://github.com/Badr1Alanzi)
- X: [@B5d2z](https://x.com/B5d2z)

## Credits

NovaDL would not exist without the incredible [yt-dlp](https://github.com/yt-dlp/yt-dlp) project and its contributors.
