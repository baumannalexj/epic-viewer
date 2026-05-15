import argparse
import logging
import re
import shutil
import subprocess
import sys

from app_view.epicviewer import EpicViewApp
from clients.atlassian_cli import AtlassianClient
from config import Config
from core.services.table_service import TableService
from repository.table_state_repository import TableStateRepository

_SITE_RE = re.compile(r"site:\s*([\w.-]+\.atlassian\.net)", re.IGNORECASE)

logging.basicConfig(level=logging.INFO)

def _parse_jira_base_url(status_output: str) -> str:
    m = _SITE_RE.search(status_output)
    if m:
        return f"https://{m.group(1)}"
    # fallback: scan for any atlassian.net hostname
    m2 = re.search(r"(https?://[\w.-]+\.atlassian\.net)", status_output)
    return m2.group(1) if m2 else "https://toasttab.atlassian.net"


def _check_auth() -> str:
    """Ensures acli is installed and authenticated. Returns the Jira base URL."""
    if not shutil.which("acli"):
        print("epicviewer: 'acli' is not installed.")
        print("  Run the following, then re-launch epicviewer:\n")
        print("    brew tap atlassian/homebrew-acli")
        print("    brew install acli\n")
        sys.exit(1)

    while True:
        result = subprocess.run(["acli", "auth", "status"], capture_output=True, text=True)
        output = (result.stdout + result.stderr).strip()
        authenticated = result.returncode == 0 and "✓ authenticated" in output.lower()

        if authenticated:
            print(output)
            answer = input("\nUse this acli auth session? [Y/n]: ").strip().lower()
            if answer in ("", "y", "yes"):
                return _parse_jira_base_url(output)

        print("\nNo active acli session (or you chose to re-authenticate).")
        print("Run this in another terminal, then press any key to continue:\n")
        print("    acli auth login\n")
        input("Press any key once logged in...")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Interactive Jira epic dashboard for a tmux pane."
    )
    parser.add_argument("epic_key", help="Jira epic key, e.g. ECPL-6126")
    args = parser.parse_args()

    jira_base_url = _check_auth()
    config = Config(jira_base_url=jira_base_url)

    client = AtlassianClient()
    repo = TableStateRepository()
    table_service = TableService(client, repo)
    EpicViewApp(args.epic_key, table_service, config).run()


if __name__ == "__main__":
    main()
