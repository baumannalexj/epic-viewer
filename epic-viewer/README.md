# epicviewer

Interactive Jira epic dashboard for a tmux pane.

```
in progress  [↓] | ECPL-6126 Build payroll-billing service
─────────────────────────────────────────────────────────
closed-done  [↓] | ECPL-6334 update bastion in staging and prod
in progress  [↓] | ECPL-6381 payroll-billing camel init
to do        [↓] | ECPL-6402 register port in svcmgmt-fixtures
blocked      [↓] | ECPL-6387 request preprod ec-mysql credentials
─────────────────────────────────────────────────────────
 r refresh   q quit
```

## Prerequisites

- [uv](https://docs.astral.sh/uv/) — `brew install uv`
- [acli](https://developer.atlassian.com/cloud/acli/):
  ```bash
  brew tap atlassian/homebrew-acli
  brew install acli
  acli auth login
  ```

## Running

From `~/toast/epic-view/`:

```bash
uv run epicviewer ECPL-6126
```

`uv` syncs dependencies automatically on first run — no manual venv setup needed.

## Keybindings

| Key | Action |
|-----|--------|
| Click `[↓]` cell | Open transition picker for that ticket |
| `r` | Refresh data from Jira |
| `q` | Quit |
| cmd-click ticket key | Open ticket in browser (requires OSC-8 terminal: iTerm2, WezTerm) |

## How it works

- Fetches the epic and its children via `acli jira workitem` commands
- Renders a `DataTable` with status (color-coded) and linked ticket key + summary
- Clicking the status cell fetches valid transitions and shows a modal picker
- Selecting a transition calls `acli jira workitem transition` and refreshes the row
- Falls back from `parent = KEY` JQL to `"Epic Link" = KEY` for older project layouts
