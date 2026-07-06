from pathlib import Path

from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from novadl.core.entities.media import DownloadResult, MediaInfo, MediaType
from novadl.core.entities.playlist import PlaylistInfo
from novadl.presentation.console import console
from novadl.utils.constants import APP_NAME, APP_VERSION


def show_welcome() -> None:
    text = Text()
    text.append(f"{APP_NAME} v{APP_VERSION}", style="bold cyan")
    text.append("\nأداة تحميل فيديوهات وصوت من الإنترنت")
    console.print(Panel(text, border_style="cyan"))


def show_info(info: MediaInfo | PlaylistInfo) -> None:
    if isinstance(info, PlaylistInfo):
        _show_playlist_info(info)
    else:
        _show_media_info(info)


def _show_media_info(info: MediaInfo) -> None:
    table = Table(box=box.ROUNDED, title="معلومات الوسائط", title_style="bold cyan")
    table.add_column("الخاصية", style="cyan")
    table.add_column("القيمة", style="white")

    table.add_row("العنوان", info.title)
    table.add_row("المدة", info.duration_str)
    table.add_row("الناشر", info.uploader or "N/A")
    table.add_row("تاريخ النشر", info.upload_date or "N/A")
    table.add_row("المصدر", info.webpage_url or info.url)
    table.add_row("المستخرج", info.extractor or "N/A")

    if info.formats:
        fmt_count = len(info.formats)
        table.add_row("الصيغ المتاحة", str(fmt_count))

    if info.subtitles:
        subs = ", ".join(info.subtitles.keys())
        table.add_row("الترجمات", subs)

    console.print(table)
    console.print()


def _show_playlist_info(info: PlaylistInfo) -> None:
    table = Table(box=box.ROUNDED, title="معلومات قائمة التشغيل", title_style="bold cyan")
    table.add_column("الخاصية", style="cyan")
    table.add_column("القيمة", style="white")

    table.add_row("العنوان", info.title)
    table.add_row("الناشر", info.uploader or "N/A")
    table.add_row("المقاطع", str(info.entry_count))
    table.add_row("المصدر", info.webpage_url or info.url)
    table.add_row("المستخرج", info.extractor or "N/A")

    console.print(table)

    if info.entries:
        entries_table = Table(box=box.SIMPLE, title="مقاطع قائمة التشغيل", title_style="bold")
        entries_table.add_column("#", style="dim")
        entries_table.add_column("العنوان", style="white")
        entries_table.add_column("المدة", style="cyan")

        for i, entry in enumerate(info.entries[:50], 1):
            entries_table.add_row(str(i), entry.title, entry.duration_str or "N/A")

        console.print(entries_table)
        if info.entry_count > 50:
            console.print(f"[dim]... و{info.entry_count - 50} مقطع آخر[/dim]")

    console.print()


def show_download_result(result: DownloadResult) -> None:
    if result.success:
        file_size_str = _format_size(result.file_size)
        console.print(f"[success]✓ تم التحميل:[/success] {result.title}")
        console.print(f"  [dim]المسار:[/dim] [path]{result.file_path}[/path]")
        console.print(f"  [dim]الحجم:[/dim] {file_size_str}")
    else:
        console.print(f"[error]✗ فشل:[/error] {result.title}")
        console.print(f"  [error]السبب:[/error] {result.error_message}")
    console.print()


def show_history(entries: list[DownloadResult]) -> None:
    if not entries:
        console.print("[dim]لا يوجد سجل تحميل.[/dim]")
        return

    table = Table(box=box.ROUNDED, title="سجل التحميل", title_style="bold cyan")
    table.add_column("#", style="dim")
    table.add_column("العنوان", style="white")
    table.add_column("النوع", style="cyan")
    table.add_column("الحجم", style="white")
    table.add_column("الحالة", style="bold")

    for i, entry in enumerate(entries[:20], 1):
        status = "[success]ناجح[/success]" if entry.success else "[error]فاشل[/error]"
        size = _format_size(entry.file_size)
        media_type = "فيديو" if entry.media_type == MediaType.VIDEO else "صوت"
        table.add_row(str(i), entry.title[:50], media_type, size, status)

    console.print(table)
    if len(entries) > 20:
        console.print(f"[dim]... و{len(entries) - 20} إدخال آخر[/dim]")
    console.print()


def show_config(config: dict[str, str]) -> None:
    if not config:
        console.print("[dim]لا يوجد إعدادات مخصصة. جميع القيم الافتراضية مفعلة.[/dim]")
        return

    table = Table(box=box.ROUNDED, title="الإعدادات الحالية", title_style="bold cyan")
    table.add_column("المفتاح", style="cyan")
    table.add_column("القيمة", style="white")

    for key, value in sorted(config.items()):
        table.add_row(key, value)

    console.print(table)
    console.print()


def show_diagnosis(ffmpeg_installed: bool, ffmpeg_version: str | None, yt_dlp_version: str) -> None:
    table = Table(box=box.ROUNDED, title="تشخيص النظام", title_style="bold cyan")
    table.add_column("المكون", style="cyan")
    table.add_column("الحالة", style="bold")
    table.add_column("الإصدار", style="white")

    yt_status = "[success]✓[/success]" if yt_dlp_version != "unknown" else "[error]✗[/error]"
    table.add_row("yt-dlp", yt_status, yt_dlp_version)

    ff_status = "[success]✓[/success]" if ffmpeg_installed else "[warning]✗ Not found[/warning]"
    table.add_row("FFmpeg", ff_status, ffmpeg_version or "N/A")

    console.print(table)
    console.print()


def _format_size(size: int) -> str:
    if size == 0:
        return "N/A"
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"
