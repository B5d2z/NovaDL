import sys
from pathlib import Path

from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from novadl.cli.commands import _config, _downloader, _download_use_case, _history
from novadl.infrastructure.system.ffmpeg_checker import FFmpegChecker
from novadl.presentation.console import console
from novadl.presentation.display import show_download_result, show_history
from novadl.presentation.progress import create_progress, make_progress_hook
from novadl.utils.constants import APP_NAME, APP_VERSION
from novadl.utils.exceptions import NovaDLError

PLATFORMS = [
    ("YouTube", "youtube.com/watch?v="),
    ("TikTok", "tiktok.com/@"),
    ("Instagram", "instagram.com/p/"),
    ("Facebook", "facebook.com/watch/"),
    ("X (Twitter)", "x.com/"),
    ("Vimeo", "vimeo.com/"),
    ("Reddit", "reddit.com/r/"),
    ("Twitch", "twitch.tv/"),
    ("SoundCloud", "soundcloud.com/"),
    ("Custom URL", ""),
]


def _get_download_dir() -> Path:
    saved = _config.get("output_dir")
    if saved:
        return Path(saved)
    return Path.home() / "Videos" / "NovaDL"


def _set_download_dir(path: str) -> None:
    resolved = Path(path).resolve()
    resolved.mkdir(parents=True, exist_ok=True)
    _config.set("output_dir", str(resolved))
    console.print(f"[success]✓ Save path set: {resolved}[/success]")


def _change_path() -> None:
    current = _get_download_dir()
    console.print(f"[info]Current path:[/info] [path]{current}[/path]")
    new_path = Prompt.ask("[cyan]New path[/cyan]", default=str(current))
    _set_download_dir(new_path)


def _get_quality() -> str:
    table = Table(box=None, show_header=False)
    table.add_column("#", style="dim")
    table.add_column("Quality")
    for i, q in enumerate(["Best quality", "1080p", "720p", "480p", "360p", "Worst quality"], 1):
        table.add_row(str(i), q)
    console.print(table)

    choice = Prompt.ask("[cyan]Choose quality[/cyan]", default="1")
    quality_map = {
        "1": "best",
        "2": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "3": "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "4": "bestvideo[height<=480]+bestaudio/best[height<=480]",
        "5": "bestvideo[height<=360]+bestaudio/best[height<=360]",
        "6": "worst",
    }
    return quality_map.get(choice, "best")


def _download_interactive(url: str, audio_only: bool = False) -> None:
    output_dir = _get_download_dir()
    output_dir.mkdir(parents=True, exist_ok=True)
    quality = _get_quality()

    try:
        with create_progress() as progress:
            task_id = progress.add_task("[cyan]Downloading...[/cyan]", total=None)
            hook = make_progress_hook(progress, task_id)

            result = _download_use_case.execute_single(
                url=url,
                output_dir=output_dir,
                quality=quality,
                audio_only=audio_only,
                audio_format=_config.get("audio_format", "mp3"),
                audio_quality=_config.get("audio_quality", "192"),
                progress_callback=hook,
            )

        show_download_result(result)
    except NovaDLError as e:
        console.print(f"[error]Error:[/error] {e}")


def _platform_menu() -> None:
    console.print()
    table = Table(box=None, show_header=False, title="Select Platform", title_style="bold cyan")
    table.add_column("#", style="dim")
    table.add_column("Platform")

    for i, (name, _) in enumerate(PLATFORMS, 1):
        table.add_row(str(i), name)

    table.add_row("11", "Change save path")
    table.add_row("12", "Download history")
    table.add_row("13", "System info")
    table.add_row("14", "Exit")
    console.print(table)

    choice = Prompt.ask("[cyan]Enter number[/cyan]", default="1")

    if choice == "11":
        _change_path()
        return
    elif choice == "12":
        show_history(_history.get_all())
        return
    elif choice == "13":
        _show_doctor()
        return
    elif choice == "14":
        console.print("[info]Goodbye![/info]")
        sys.exit(0)

    idx = int(choice) - 1
    if idx < 0 or idx >= len(PLATFORMS):
        console.print("[error]Invalid choice[/error]")
        return

    platform_name, url_hint = PLATFORMS[idx]

    if not url_hint:
        url = Prompt.ask("[cyan]Enter URL[/cyan]")
    else:
        console.print(f"[dim]Example: https://www.{url_hint}...[/dim]")
        url = Prompt.ask(f"[cyan]Enter {platform_name} URL[/cyan]")

    media_type = Prompt.ask("[cyan]Video or Audio?[/cyan]", choices=["1", "2"], default="1")
    audio_only = media_type == "2"

    if audio_only:
        console.print(f"[info]Downloading audio from {platform_name}[/info]")
    else:
        console.print(f"[info]Downloading video from {platform_name}[/info]")

    _download_interactive(url, audio_only)


def _show_doctor() -> None:
    import platform as pf

    console.print(f"[bold cyan]NovaDL v{APP_VERSION}[/bold cyan]")
    console.print()
    dt = Table(box=None, show_header=False)
    dt.add_column("Component", style="cyan")
    dt.add_column("Value", style="white")
    dt.add_row("OS", f"{pf.system()} {pf.release()}")
    dt.add_row("Python", pf.python_version())
    dt.add_row("yt-dlp", _downloader.get_version())
    dt.add_row("FFmpeg", "Installed" if FFmpegChecker.is_installed() else "Not found")
    console.print(dt)
    console.print()


def run() -> None:
    show_welcome = True
    while True:
        if show_welcome:
            console.print(Panel(f"[bold cyan]{APP_NAME} v{APP_VERSION}[/bold cyan]\nDownload video & audio from YouTube, TikTok, Instagram, and 1000+ sites.\n[dim]Developer: {APP_AUTHOR} | X: {APP_X} | GitHub: {APP_GITHUB}[/dim]", border_style="cyan"))
            show_welcome = False

        path = _get_download_dir()
        console.print(f"[dim]Save path: [path]{path}[/path][/dim]")
        console.print()

        _platform_menu()

        if not Confirm.ask("[cyan]Back to main menu?[/cyan]", default=True):
            console.print("[info]Goodbye![/info]")
            break
        console.print()
