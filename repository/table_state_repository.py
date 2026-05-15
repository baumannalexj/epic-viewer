from core.models.issue_model import IssueModel
from core.ports.i_table_state_repository import ITableStateRepository


class TableStateRepository(ITableStateRepository):
    def __init__(self) -> None:
        self._store: dict[str, IssueModel] = {}

    def save_issues(self, issues: list[IssueModel]) -> None:
        self._store = {issue.key: issue for issue in issues}

    def save_issue(self, issue: IssueModel) -> None:
        self._store[issue.key] = issue

    def get_issue_by_key(self, key: str) -> IssueModel | None:
        return self._store.get(key)

    def get_issues(self) -> list[IssueModel]:
        return list(self._store.values())
