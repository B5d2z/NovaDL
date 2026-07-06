from pathlib import Path
from typing import Optional

import typer

from novadl.cli.callbacks import resolve_output_dir, validate_cookies, validate_url
from novadl.core.use_cases.download import DownloadUseCase
from novadl.core.use_cases.extract_info import ExtractInfoUseCase
from novadl.core.use_cases.update import UpdateUseCase
from novadl.infrastructure.config.config_manager import ConfigManager
from novadl.infrastructure.downloader.yt_dlp_downloader import YtDlpDownloader
from novadl.infrastructure.history.history_manager import HistoryManager
from novadl.infrastructure.system.ffmpeg_checker import FFmpegChecker
from novadl.presentation.console import console
from novadl.presentation.display import (
    show_config,
    show_diagnosis,
    show_download_result,
    show_history,
    show_info,
)
from novadl.presentation.progress import create_progress, make_progress_hook
from novadl.utils.constants import APP_AUTHOR, APP_GITHUB, APP_NAME, APP_VERSION, APP_X
from novadl.utils.exceptions import NovaDLError

_downloader = YtDlpDownloader()
_config = ConfigManager()
_history = HistoryManager()
_download_use_case = DownloadUseCase(_downloader, _config, _history)
_info_use_case = ExtractInfoUseCase(_downloader)
_update_use_case = UpdateUseCase(_downloader)


def download(
    url: str = typer.Argument(..., help="URL of the video to download", callback=validate_url),
    output_dir: Optional[str] = typer.Option(None, "--output-dir", "-o", help="Output directory", callback=resolve_output_dir),
    quality: Optional[str] = typer.Option(None, "--quality", "-q", help="Video quality (best, worst, bestvideo, worstvideo)"),
    format: Optional[str] = typer.Option(None, "--format", "-f", help="Output format (mp4, mkv, webm, etc.)"),
    audio_only: bool = typer.Option(False, "--audio-only", "-a", help="Download audio only"),
    audio_format: str = typer.Option("mp3", "--audio-format", help="Audio format (mp3, m4a, opus, flac, wav)"),
    audio_quality: str = typer.Option("192", "--audio-quality", help="Audio quality in kbps"),
    subtitles: bool = typer.Option(False, "--subtitles", "-s", help="Download subtitles"),
    subtitle_langs: Optional[str] = typer.Option(None, "--sub-langs", help="Subtitle language codes (comma separated)"),
    embed_subs: bool = typer.Option(False, "--embed-subs", help="Embed subtitles into video"),
    write_thumbnail: bool = typer.Option(False, "--thumbnail", "-t", help="Write thumbnail"),
    cookies: Optional[str] = typer.Option(None, "--cookies", "-c", help="Path to cookies file", callback=validate_cookies),
    proxy: Optional[str] = typer.Option(None, "--proxy", "-p", help="Proxy URL"),
) -> None:
    try:
        with create_progress() as progress:
            task_id = progress.add_task(f"[cyan]Downloading:[/cyan] {url[:60]}", total=None)
            hook = make_progress_hook(progress, task_id)

            sub_langs = subtitle_langs.split(",") if subtitle_langs else None
            result = _download_use_case.execute_single(
                url=url,
                output_dir=output_dir,
                quality=quality,
                audio_only=audio_only,
                audio_format=audio_format,
                audio_quality=audio_quality,
                output_format=format,
                subtitles=subtitles,
                subtitle_langs=sub_langs,
                embed_subs=embed_subs,
                write_thumbnail=write_thumbnail,
                cookies_file=cookies,
                proxy_url=proxy,
                progress_callback=hook,
            )

        show_download_result(result)
    except NovaDLError as e:
        console.print(f"[error]Error:[/error] {e}")
        raise typer.Exit(1)


def audio(
    url: str = typer.Argument(..., help="URL of the video to extract audio from", callback=validate_url),
    output_dir: Optional[str] = typer.Option(None, "--output-dir", "-o", help="Output directory", callback=resolve_output_dir),
    audio_format: str = typer.Option("mp3", "--format", "-f", help="Audio format (mp3, m4a, opus, flac, wav)"),
    audio_quality: str = typer.Option("192", "--quality", "-q", help="Audio quality in kbps"),
    cookies: Optional[str] = typer.Option(None, "--cookies", "-c", help="Path to cookies file", callback=validate_cookies),
    proxy: Optional[str] = typer.Option(None, "--proxy", "-p", help="Proxy URL"),
) -> None:
    try:
        with create_progress() as progress:
            task_id = progress.add_task(f"[cyan]Extracting audio:[/cyan] {url[:60]}", total=None)
            hook = make_progress_hook(progress, task_id)

            result = _download_use_case.execute_single(
                url=url,
                output_dir=output_dir,
                audio_only=True,
                audio_format=audio_format,
                audio_quality=audio_quality,
                cookies_file=cookies,
                proxy_url=proxy,
                progress_callback=hook,
            )

        show_download_result(result)
    except NovaDLError as e:
        console.print(f"[error]Error:[/error] {e}")
        raise typer.Exit(1)


def info(
    url: str = typer.Argument(..., help="URL to extract information from", callback=validate_url),
) -> None:
    try:
        media_info = _info_use_case.execute(url)
        show_info(media_info)
    except NovaDLError as e:
        console.print(f"[error]Error:[/error] {e}")
        raise typer.Exit(1)


def update() -> None:
    try:
        with console.status("[cyan]Updating yt-dlp...[/cyan]"):
            updated = _update_use_case.execute()
        if updated:
            console.print("[success]✓ yt-dlp updated successfully[/success]")
        else:
            console.print("[info]yt-dlp is already up to date[/info]")
    except NovaDLError as e:
        console.print(f"[error]Error:[/error] {e}")
        raise typer.Exit(1)


def config(
    key: Optional[str] = typer.Argument(None, help="Configuration key to view or set"),
    value: Optional[str] = typer.Argument(None, help="Value to set"),
) -> None:
    try:
        if key and value:
            _config.set(key, value)
            console.print(f"[success]✓ Set {key} = {value}[/success]")
        elif key:
            current = _config.get(key)
            if current is not None:
                console.print(f"[info]{key}[/info] = [white]{current}[/white]")
            else:
                console.print(f"[dim]No value set for '{key}'[/dim]")
        else:
            show_config(_config.get_all())
    except NovaDLError as e:
        console.print(f"[error]Error:[/error] {e}")
        raise typer.Exit(1)


def version() -> None:
    console.print(f"[bold cyan]{APP_NAME}[/bold cyan] [white]v{APP_VERSION}[/white]")
    console.print(f"Author: {APP_AUTHOR}")
    console.print(f"GitHub: {APP_GITHUB}")
    console.print(f"X: {APP_X}")
    console.print(f"yt-dlp engine: {_downloader.get_version()}")


def history() -> None:
    entries = _history.get_all()
    show_history(entries)


def clear_history() -> None:
    _history.clear()
    console.print("[success]✓ Download history cleared[/success]")


def doctor() -> None:
    import platform

    console.print(f"OS: {platform.system()} {platform.release()}")
    console.print(f"Python: {platform.python_version()}")
    console.print(f"{APP_NAME}: v{APP_VERSION}")

    ffmpeg_installed = FFmpegChecker.is_installed()
    ffmpeg_version = FFmpegChecker.get_version()
    yt_dlp_version = _downloader.get_version()

    show_diagnosis(ffmpeg_installed, ffmpeg_version, yt_dlp_version)

    if not ffmpeg_installed:
        console.print("[warning]FFmpeg not found[/warning]")
        console.print(FFmpegChecker.get_install_guide())
