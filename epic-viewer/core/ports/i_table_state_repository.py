from abc import ABC, abstractmethod

from core.models.issue_model import IssueModel


class ITableStateRepository(ABC):
    @abstractmethod
    def save_issues(self, issues: list[IssueModel]) -> None: ...

    @abstractmethod
    def save_issue(self, issue: IssueModel) -> None: ...

    @abstractmethod
    def get_issue_by_key(self, key: str) -> IssueModel | None: ...

    @abstractmethod
    def get_issues(self) -> list[IssueModel]: ...
