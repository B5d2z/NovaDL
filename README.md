# NovaDL

Download video & audio from YouTube, TikTok, Instagram, Facebook, X (Twitter), Vimeo, Reddit, Twitch, SoundCloud, and 1000+ sites — right from your terminal.

Built on [yt-dlp](https://github.com/yt-dlp/yt-dlp).

## Features

- **Video & Audio** — Download from any site yt-dlp supports
- **Audio extraction** — MP3, M4A, Opus, FLAC, WAV
- **Quality selection** — Best, 1080p, 720p, 480p, 360p, Worst
- **Playlist support** — Download entire channels and playlists
- **Subtitles** — Download and embed subtitles
- **Thumbnails** — Download thumbnail images
- **Resume** — Continue interrupted downloads
- **Cookies** — Authenticated downloads via cookies file
- **Proxy** — Route through a proxy
- **History** — Track past downloads
- **Config** — Persistent settings
- **yt-dlp update** — Update the engine from the CLI
- **FFmpeg check** — Detect FFmpeg and show install guide
- **Interactive menu** — Numbered selection interface
- **Progress bars** — Speed, ETA, file size, percentage

## Requirements

- Python 3.8+
- [FFmpeg](https://ffmpeg.org/) (required for audio extraction & format conversion)

## Quick start

```bash
git clone https://github.com/Badr1Alanzi/novadl.git
cd novadl
python run.py
```

## Usage

### Interactive menu

```bash
python run.py
```

Select a platform by number, choose video or audio, enter the URL, pick quality, and download.

### Direct commands

```bash
python run.py download "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
python run.py audio "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
python run.py info "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
python run.py update
python run.py config
python run.py version
python run.py history
python run.py clear-history
python run.py doctor
```

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--output-dir` | `-o` | Output directory |
| `--quality` | `-q` | Video quality |
| `--format` | `-f` | Output format (mp4, mkv, webm) |
| `--audio-only` | `-a` | Audio only |
| `--audio-format` | | Audio format |
| `--audio-quality` | | Audio quality in kbps |
| `--subtitles` | `-s` | Download subtitles |
| `--sub-langs` | | Language codes (comma separated) |
| `--embed-subs` | | Embed subtitles |
| `--thumbnail` | `-t` | Write thumbnail |
| `--cookies` | `-c` | Cookies file path |
| `--proxy` | `-p` | Proxy URL |

## Commands

| Command | Description |
|---------|-------------|
| `python run.py download <url>` | Download video |
| `python run.py audio <url>` | Download audio only |
| `python run.py info <url>` | Show media information |
| `python run.py update` | Update yt-dlp |
| `python run.py config [key] [val]` | View or set configuration |
| `python run.py version` | Show version info |
| `python run.py history` | Show download history |
| `python run.py clear-history` | Clear history |
| `python run.py doctor` | System diagnosis |

## Config

Stored in `~/.config/novadl/config.json`.

```bash
python run.py config                        # view all
python run.py config output_dir             # view one key
python run.py config output_dir "~/Videos"  # set a value
```

| Key | Default | Description |
|-----|---------|-------------|
| `output_dir` | `~/Videos/NovaDL` | Download directory |
| `proxy` | — | Default proxy |
| `cookies` | — | Default cookies file |
| `audio_format` | `mp3` | Default audio format |
| `audio_quality` | `192` | Default audio quality (kbps) |

## Project structure

```
novadl/
├── run.py            # Single entry point
├── pyproject.toml
├── README.md
├── LICENSE
└── src/novadl/
    ├── __init__.py   # Version info
    ├── const.py      # Constants, exceptions, logger
    ├── core.py       # Entities, interfaces, use cases
    ├── infra.py      # yt-dlp, config, history, ffmpeg
    ├── ui.py         # Rich terminal UI
    └── cli.py        # Commands + interactive menu + app
```

## FAQ

**Q: Do I need FFmpeg?**
A: Yes for audio extraction and format conversion. Run `python run.py doctor` for install instructions.

**Q: Can I download private videos?**
A: Yes, use `--cookies` with a cookies file from your browser.

**Q: Supported platforms?**
A: Windows, macOS, Linux.

## License

MIT — see [LICENSE](LICENSE).

## Developer

**Badr Alanzi** — [GitHub](https://github.com/Badr1Alanzi) | [X](https://x.com/B5d2z)
