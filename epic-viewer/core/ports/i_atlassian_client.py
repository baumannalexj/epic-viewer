from abc import ABC, abstractmethod

from core.models.issue_model import IssueModel, IssueStatus


class IAtlassianClient(ABC):
    @abstractmethod
    def fetch_parent(self, key: str) -> IssueModel: ...

    @abstractmethod
    def fetch_children(self, parent_key: str) -> list[IssueModel]: ...

    @abstractmethod
    def fetch_available_statuses(self, key: str) -> list[IssueStatus]: ...

    @abstractmethod
    def set_issue_status(self, key: str, status: IssueStatus) -> None: ...
