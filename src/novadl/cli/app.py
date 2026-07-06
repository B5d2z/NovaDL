import typer

from novadl import __version__
from novadl.cli.commands import (
    audio,
    clear_history,
    config,
    doctor,
    download,
    history,
    info,
    update,
    version,
)
from novadl.presentation.console import console
from novadl.presentation.display import show_welcome

app = typer.Typer(
    name="novadl",
    help="A powerful CLI downloader for video and audio from the internet.",
    no_args_is_help=True,
    rich_markup_mode="rich",
    pretty_exceptions_show_locals=False,
)

app.command(name="download")(download)
app.command(name="audio")(audio)
app.command(name="info")(info)
app.command(name="update")(update)
app.command(name="config")(config)
app.command(name="version")(version)
app.command(name="history")(history)
app.command(name="clear-history")(clear_history)
app.command(name="doctor")(doctor)


def main() -> None:
    show_welcome()
    app()


if __name__ == "__main__":
    main()
