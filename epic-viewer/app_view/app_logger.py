import logging
from datetime import datetime

from textual.widgets import RichLog


def create_log_widget() -> RichLog:
    return RichLog(id="log", highlight=True, markup=True, wrap=False, max_lines=50)


def get_logger(name: str) -> logging.Logger:
    """Return a logger under the epicviewer.* hierarchy — shows %(name)s in output."""
    return logging.getLogger(f"epicviewer.{name}")


def attach_log_handler(log_widget: RichLog) -> None:
    """Wire the RichLog widget to all epicviewer.* loggers. Call once on mount."""
    root = logging.getLogger("epicviewer")
    root.setLevel(logging.DEBUG)
    root.addHandler(AppLogHandler(log_widget))


class AppLogHandler(logging.Handler):
    def __init__(self, log_widget: RichLog) -> None:
        super().__init__()
        self._log_widget = log_widget

    def emit(self, record: logging.LogRecord) -> None:
        ts = datetime.now().strftime("%H:%M:%S")
        level_colors = {
            logging.WARNING: "yellow",
            logging.ERROR: "red",
            logging.INFO: "dim",
        }
        color = level_colors.get(record.levelno, "white")
        source = record.name.removeprefix("epicviewer.")
        self._log_widget.write(
            f"[dim]{ts}[/dim]  [{color}]{source}: {record.getMessage()}[/{color}]"
        )
