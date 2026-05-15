from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.models.issue_model import EpicModel, IssueModel, IssueStatus


@dataclass
class StatusDto:
    name: str
    category_key: str
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> StatusDto:
        category = d.get("statusCategory") or {}
        return cls(
            name=d.get("name", "unknown"),
            category_key=category.get("key", "new"),
            extra={k: v for k, v in d.items() if k not in ("name", "statusCategory")},
        )

    def to_issue_status(self) -> IssueStatus:
        return IssueStatus(name=self.name, category=self.category_key)


@dataclass
class IssueDto:
    key: str
    summary: str
    status: StatusDto
    issue_type: str
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> IssueDto:
        fields = d.get("fields") or {}
        issuetype = fields.get("issuetype") or {}
        return cls(
            key=d.get("key", ""),
            summary=fields.get("summary", ""),
            status=StatusDto.from_dict(fields.get("status") or {}),
            issue_type=issuetype.get("name", ""),
            extra={k: v for k, v in d.items() if k not in ("key", "fields")},
        )

    def to_model(self) -> IssueModel:
        if self.issue_type == "Epic":
            return EpicModel(
                key=self.key,
                summary=self.summary,
                status=self.status.to_issue_status(),
            )
        return IssueModel(
            key=self.key,
            summary=self.summary,
            status=self.status.to_issue_status(),
        )
