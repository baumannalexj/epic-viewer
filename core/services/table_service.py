from core.models.issue_model import IssueModel, IssueStatus
from core.ports.i_atlassian_client import IAtlassianClient
from core.ports.i_table_state_repository import ITableStateRepository


class TableService:
    def __init__(self, client: IAtlassianClient, repo: ITableStateRepository) -> None:
        self._client = client
        self._repo = repo

    # todo claude - rename this as initial_load_parent_and_issues
    def get_parent_and_issues(self, parent_key: str) -> list[IssueModel]:
        parent = self._client.fetch_parent(parent_key)
        children = self._client.fetch_children(parent_key)
        issues = [parent] + children
        self._repo.save_issues(issues)
        return issues

    def get_issues(self) -> list[IssueModel]:
        return self._repo.get_issues()

    def get_issue_by_key(self, key: str) -> IssueModel | None:
        return self._repo.get_issue_by_key(key)

    def get_available_statuses(self, issue_key: str) -> list[IssueStatus]:
        return self._client.fetch_available_statuses(issue_key)

    def set_issue_status(self, issue_key: str, status: IssueStatus) -> None:
        self._client.set_issue_status(issue_key, status)
