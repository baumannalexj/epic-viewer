
import webbrowser
from abc import ABC, abstractmethod

from textual.widgets import DataTable

from app_view.views import ColumnType, TableRowView, TableModal

from textual.app import App
from config import Config
from core.models.issue_model import IssueStatus
from core.services.table_service import TableService


class CellHandlerFactory:
    def __init__(self, app: App, table_service: TableService, config: Config) -> None:
        self._app = app
        self._table_service = table_service
        self._config = config

    def get_handler(self, table_row_key: str, table_column_key: str, table: DataTable) -> "CellActionHandler":

        if table_row_key == self._config.SEPARATOR_KEY:
            return CellHandlerFactory.NoOpCellHandler()

        match table_column_key:

            case ColumnType.STATUS:
                return CellHandlerFactory.StatusCellHandler(self._app, self._table_service, table_row_key)

            # case ColumnType.ISSUE:
            case _:
                return CellHandlerFactory.IssueCellHandler(self._table_service, self._config, table, table_row_key)



    class CellActionHandler(ABC):
        @abstractmethod
        def on_hover(self) -> None:
            ...

        @abstractmethod
        def on_click(self) -> None:
            ...

    class NoOpCellHandler(CellActionHandler):
        def on_hover(self) -> None:
            """don't do anything"""
            pass

        def on_click(self) -> None:
            """don't do anything"""
            pass

    class IssueCellHandler(CellActionHandler):
        def __init__(self,
                     table_service: TableService,
                     config: Config,
                     data_table: DataTable,
                     row_key: str) -> None:
            self._table = data_table
            self._row_key = row_key
            self._table_service = table_service
            self._config = config

        def on_hover(self) -> None:
            issue = self._table_service.get_issue_by_key(self._row_key)
            if issue:
                row = TableRowView.from_issue(issue, self._config)
                self._table.update_cell(self._row_key, ColumnType.ISSUE, row.hovered_issue_cell)

        def on_click(self) -> None:
            issue = self._table_service.get_issue_by_key(self._row_key)
            if issue:
                row = TableRowView.from_issue(issue, self._config)
                webbrowser.open(row.url)

    class StatusCellHandler(CellActionHandler):
        def __init__(self, app: App, table_service: TableService, row_key: str) -> None:
            self._app = app
            self._row_key = row_key
            self._table_service = table_service

        def on_hover(self) -> None:
            pass

        def on_click(self) -> None:

            statuses = self._table_service.get_available_statuses(self._row_key)
            if not statuses:
                return

            def apply(status: IssueStatus | None) -> None:
                if status:
                    self._table_service.set_issue_status(self._row_key, status)

            self._app.push_screen(TableModal(self._row_key, statuses), apply)

