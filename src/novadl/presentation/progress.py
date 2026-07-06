from typing import Any

from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)


def create_progress() -> Progress:
    return Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        transient=False,
    )


def make_progress_hook(progress: Progress, task_id: int):
    def hook(d: dict[str, Any]) -> None:
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
            downloaded = d.get("downloaded_bytes", 0)
            progress.update(task_id, completed=downloaded, total=total)
        elif d["status"] == "finished":
            progress.update(task_id, completed=d.get("total_bytes", 0))

    return hook
