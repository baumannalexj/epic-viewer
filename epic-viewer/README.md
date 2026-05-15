# epicviewer

Interactive Jira epic dashboard for a tmux pane.

```
in progress  [↓] | PRJCT-123 Create a terminal based epic viewer
─────────────────────────────────────────────────────────
closed-done  [↓] | PRJCT-424 create repo
in progress  [↓] | PRJCT-532 create base app 
to do        [↓] | PRJCT-432 handle status changes
blocked      [↓] | PRJCT-235 handle crashes
─────────────────────────────────────────────────────────
 r refresh   q quit
```

## Prerequisites

- [uv](https://docs.astral.sh/uv/)
  - `brew install uv`
- [acli](https://developer.atlassian.com/cloud/acli/):
  ```bash
  brew tap atlassian/homebrew-acli
  brew install acli
  acli auth login
  ```

## Running

```bash
git@github.com:baumannalexj/epic-viewer.git
cd epic-view
uv run epicviewer PRJCT-123
```

Or add to your path to run anywhere

```bash
cd epic-view
uv tool install
cd somewhere/else
epicviewr
```


## Keybindings

| Key | Action |
|-----|--------|
| `r` | Refresh data from Jira |
| `q` | Quit |
| double click on a row | Open ticket in browser |

## How

- Fetches the epic and its children via `acli jira workitem` commands
- Renders a `DataTable` with status (color-coded) and linked ticket key + summary
- Clicking the status cell fetches valid transitions and shows a modal picker
- Falls back from `parent = KEY` JQL to `"Epic Link" = KEY` for older project layouts

## ToDo
- Click `[↓]` cell to change ticket status
