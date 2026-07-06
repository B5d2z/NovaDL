from pathlib import Path
from typing import Optional

import typer


def validate_url(url: str) -> str:
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        raise typer.BadParameter("URL must start with http:// or https://")
    return url


def resolve_output_dir(path: Optional[str]) -> Optional[Path]:
    if path is None:
        return None
    return Path(path).resolve()


def validate_cookies(path: Optional[str]) -> Optional[Path]:
    if path is None:
        return None
    p = Path(path)
    if not p.exists():
        raise typer.BadParameter(f"Cookies file not found: {path}")
    return p
