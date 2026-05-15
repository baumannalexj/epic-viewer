from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.models.issue_model import IssueStatus


@dataclass
class TransitionDto:
    name: str
    transition_id: str
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> TransitionDto:
        return cls(
            name=d.get("name", ""),
            transition_id=d.get("id", ""),
            extra={k: v for k, v in d.items() if k not in ("name", "id")},
        )

    def to_issue_status(self) -> IssueStatus:
        return IssueStatus(name=self.name)
