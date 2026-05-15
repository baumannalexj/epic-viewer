from dataclasses import dataclass


@dataclass
class IssueStatus:
    name: str
    category: str = ""

    def is_blocked(self) -> bool:
        return "block" in self.name.lower()


@dataclass
class IssueModel:
    key: str
    summary: str
    status: IssueStatus


@dataclass
class EpicModel(IssueModel):
    pass
