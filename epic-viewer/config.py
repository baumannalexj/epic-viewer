from dataclasses import dataclass


@dataclass
class Config:
    jira_base_url: str
    ISSUE_SUMMARY_MAX: int = 80
    SEPARATOR_KEY = "__separator__"
