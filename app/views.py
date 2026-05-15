from dataclasses import dataclass
from enum import StrEnum

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.widgets import Label, OptionList
from textual.widgets._option_list import Option

from config import Config
from core.models.issue_model import IssueStatus, IssueModel


class ColumnType(StrEnum):
    STATUS = "status"
    ISSUE = "issue"


class TableModal(ModalScreen[IssueStatus | None]):
    BINDINGS = [Binding("escape", "dismiss(None)", "Cancel")]

    def __init__(self, key: str, statuses: list[IssueStatus]) -> None:
        super().__init__()
        self._key = key
        self._statuses = statuses

    def compose(self) -> ComposeResult:
        yield Label(f"Set status: {self._key}", id="modal-title")
        yield OptionList(*[Option(s.name) for s in self._statuses], id="status-list")

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        name = str(event.option.prompt)
        selected = next((s for s in self._statuses if s.name == name), None)
        self.dismiss(selected)


class StatusCategoryColor(StrEnum):
    DONE = "green"
    INDETERMINATE = "yellow"
    BLOCKED = "red"
    NEW = "dim"
    UNKNOWN = "white"

    @classmethod
    def _missing_(cls, value: object) -> "StatusCategoryColor":
        return cls.__members__.get(str(value).upper(), cls.UNKNOWN)


@dataclass
class TableRowView:
    key: str
    url: str
    status_cell: str
    issue_cell: str

    @property
    def hovered_issue_cell(self) -> str:
        return f"[blue underline]{self.issue_cell}[/blue underline]"

    @classmethod
    def from_issues(cls, issues: list[IssueModel], config: Config) -> list["TableRowView"]:
        return [cls.from_issue(issue, config) for issue in issues]

    @classmethod
    def from_issue(cls, issue: IssueModel, config: Config) -> "TableRowView":
        summary = issue.summary
        if len(summary) > config.ISSUE_SUMMARY_MAX:
            summary = summary[:config.ISSUE_SUMMARY_MAX - 3] + "..."

        color = cls._status_color(issue.status)
        slug = cls._slugify_status(issue.status)
        url = cls._issue_url(config, issue.key)

        # \[↓] escapes the bracket so Rich doesn't parse it as a tag
        status_cell = f"\\[↓]  [{color}]{slug}[/{color}]"

        safe_summary = summary.replace("[", "\\[")
        issue_cell = f"{issue.key}  {safe_summary}"

        return cls(key=issue.key, url=url, status_cell=status_cell, issue_cell=issue_cell)

    @staticmethod
    def _status_color(status: IssueStatus) -> str:
        if status.is_blocked():
            return StatusCategoryColor.BLOCKED
        return StatusCategoryColor(status.category)

    @staticmethod
    def _slugify_status(issue_status: IssueStatus) -> str:
        return issue_status.name.lower().replace(" - ", "-")

    @staticmethod
    def _issue_url(config: Config, key: str) -> str:
        return f"{config.jira_base_url.rstrip('/')}/browse/{key}"
