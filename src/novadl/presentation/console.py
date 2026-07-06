from rich.console import Console
from rich.theme import Theme

novadl_theme = Theme(
    {
        "info": "bold cyan",
        "success": "bold green",
        "warning": "bold yellow",
        "error": "bold red",
        "title": "bold white",
        "path": "blue",
        "url": "underline blue",
        "dim": "dim white",
        "highlight": "magenta",
    }
)

console = Console(theme=novadl_theme, highlight=False)
