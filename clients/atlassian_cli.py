import json
import logging
import subprocess
from typing import Any

from clients.dto.issue_dto import IssueDto
from core.errors import ClientError, ClientNotFoundError, IssueNotFoundError
from core.models.issue_model import IssueModel, IssueStatus
from core.ports.i_atlassian_client import IAtlassianClient


class AtlassianClient(IAtlassianClient):
    def _run(self, *args: str) -> Any:
        try:
            result = subprocess.run(
                ["acli", *args],
                capture_output=True,
                text=True,
                check=True,
            )
        except FileNotFoundError:
            logging.error("acli not found on PATH")
            raise ClientNotFoundError("acli not found on PATH. Install: brew tap atlassian/homebrew-acli && brew install acli")
        except subprocess.CalledProcessError as e:
            msg = e.stderr.strip()
            logging.error(f"acli error: {msg}")
            raise ClientError(msg)

        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return result.stdout.strip()

    def fetch_parent(self, key: str) -> IssueModel:
        raw = self._run("jira", "workitem", "view", key, "--json")
        if not isinstance(raw, dict):
            raise IssueNotFoundError(key)
        return IssueDto.from_dict(raw).to_model()

    def fetch_children(self, parent_key: str) -> list[IssueModel]:
        raw = self._run(
            "jira", "workitem", "search",
            "--jql", f"parent = {parent_key}",
            "--json",
        )
        if isinstance(raw, list) and raw:
            return [IssueDto.from_dict(d).to_model() for d in raw]
        fallback = self._run(
            "jira", "workitem", "search",
            "--jql", f'"Epic Link" = {parent_key}',
            "--json",
        )
        if isinstance(fallback, list):
            return [IssueDto.from_dict(d).to_model() for d in fallback]
        return []

    def fetch_available_statuses(self, key: str) -> list[IssueStatus]:
        logging.warning("status change not implemented — cannot determine available statuses using the acli client")
        return [IssueStatus(name="n/a")]

    def set_issue_status(self, key: str, status: IssueStatus) -> None:
        logging.warning("status change not implemented")

