from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import DataTable, Footer, RichLog

from app_view.app_logger import attach_log_handler, create_log_widget
from app_view.cell_handlers import CellHandlerFactory
from app_view.views import ColumnType, TableRowView
from config import Config
from core.errors import IssueNotFoundError
from core.models.issue_model import IssueModel
from core.services.table_service import TableService


class EpicViewApp(App):
    CSS = """
    Screen { background: $surface; }

    DataTable { height: 1fr; }

    #log {
        height: 3;
        border-top: solid $surface-lighten-2;
        padding: 0 1;
        background: $surface-darken-1;
    }

    #modal-title {
        padding: 1 2;
        text-style: bold;
    }

    TableModal {
        align: center middle;
    }

    TableModal > OptionList {
        width: 60;
        max-height: 20;
        border: round $primary;
        padding: 0 1;
    }
    """

    BINDINGS = [
        Binding("r", "refresh", "Refresh"),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self, parent_issue_key: str, table_service: TableService, config: Config) -> None:
        super().__init__()
        self._issue_parent = parent_issue_key.upper()
        self._table_service = table_service
        self._config = config
        self._cellHandlerFactory = CellHandlerFactory(self, table_service, config)

    def compose(self) -> ComposeResult:
        yield DataTable(show_header=False, cursor_type="cell", zebra_stripes=True)
        yield create_log_widget()
        yield Footer()

    def on_mount(self) -> None:
        attach_log_handler(self.query_one("#log", RichLog))
        table = self.query_one(DataTable)
        table.add_column(ColumnType.STATUS, key=ColumnType.STATUS)
        table.add_column(ColumnType.ISSUE, key=ColumnType.ISSUE)
        self._show_loading()
        self.call_after_refresh(self._load)

    def _show_loading(self) -> None:
        table = self.query_one(DataTable)
        table.clear()
        table.add_row(f"Fetching {self._issue_parent}", "...", key="__loading_parent__")
        table.add_row("─" * 20, "─" * 60, key=self._config.SEPARATOR_KEY)
        table.add_row(f"Fetching workitems for {self._issue_parent}", "...", key="__loading_children__")

    def _load(self) -> None:
        table = self.query_one(DataTable)
        table.clear()
        try:
            issues: list[IssueModel] = self._table_service.get_parent_and_issues(self._issue_parent)
        except IssueNotFoundError as e:
            new_key = input(f"Issue {e.key} not found. Enter a new key: ").strip().upper()
            self._issue_parent = new_key
            self._load()
            return

        rows = TableRowView.from_issues(issues, self._config)
        parent, *children = rows

        table.add_row(parent.status_cell, parent.issue_cell, key=parent.key)
        table.add_row("─" * 20, "─" * 60, key=self._config.SEPARATOR_KEY)
        for row in children:
            table.add_row(row.status_cell, row.issue_cell, key=row.key)

    def on_data_table_cell_highlighted(self, event: DataTable.CellHighlighted) -> None:
        table = self.query_one(DataTable)
        highlighted_row_key = event.cell_key.row_key.value
        highlighted_column_key = event.cell_key.column_key.value

        for issue in self._table_service.get_issues():
            row = TableRowView.from_issue(issue, self._config)
            table.update_cell(row.key, ColumnType.ISSUE, row.issue_cell)

        self._cellHandlerFactory.\
            get_handler(highlighted_row_key, highlighted_column_key, table)\
            .on_hover()

    def on_data_table_cell_selected(self, event: DataTable.CellSelected) -> None:
        selected_column_key = event.cell_key.column_key.value
        selected_row_key = event.cell_key.row_key.value

        table = self.query_one(DataTable)
        self._cellHandlerFactory\
            .get_handler(selected_row_key, selected_column_key, table)\
            .on_click()

    def action_refresh(self) -> None:
        self._show_loading()
        self.call_after_refresh(self._load)
