# herdr keybindings

Reference for herdr 0.9.1. Source of truth: `herdr --default-config` (the
`[keys]` section) plus my overrides in `~/.config/herdr/config.toml`.
In herdr itself, `prefix` `?` shows the live list.

**Prefix:** `ctrl+b` (same as tmux). `prefix+x` means press `ctrl+b`, release,
then press `x`.

## Jeff's Goto

| Keys | Action |
|---|---|
| `prefix` `b` | Toggle sidebar |
| `prefix` `o` | Jump to the target of the latest notification |
| `prefix` `1`..`9` | Switch to tab N |
| `prefix` `v` | Split vertical (side by side) |
| `prefix` `-` | Split horizontal (stacked) |
| `prefix` `h` / `j` / `k` / `l` | Focus pane left / down / up / right |
| `prefix` `tab` | Cycle to next pane |
| `prefix` `shift+tab` | Cycle to previous pane |
| `prefix` `z` | Zoom (fullscreen) the pane |


Opened with `prefix` `g`. These plain keys apply only while it is open.

| Keys | Action |
|---|---|
| `up` / `down` | Move between workspaces |
| `h` / `j` / `k` / `l` | Focus pane left / down / up / right |

From `~/.config/herdr/config.toml` (herdr-file-viewer plugin):

| Keys | Action |
|---|---|
| `prefix` `f` | Open file viewer in a split |
| `prefix` `shift+f` | Open file viewer in a new tab |

`-------------------------------------------------------`

## Session and general

| Keys | Action |
|---|---|
| `prefix` `?` | Help / show all keybindings |
| `prefix` `s` | Settings |
| `prefix` `q` | Detach (session keeps running) |
| `prefix` `shift+r` | Reload config |
| `prefix` `o` | Jump to the target of the latest notification |
| `prefix` `b` | Toggle sidebar |
| `ctrl+v` | Paste image (only in `herdr --remote`) |

## Workspaces and worktrees

| Keys | Action |
|---|---|
| `prefix` `w` | Workspace picker |
| `prefix` `g` | Go to (navigate mode, see below) |
| `prefix` `shift+n` | New workspace |
| `prefix` `shift+g` | New git worktree |
| `prefix` `shift+w` | Rename workspace |
| `prefix` `shift+d` | Close workspace (asks to confirm) |

## Tabs

| Keys | Action |
|---|---|
| `prefix` `c` | New tab |
| `prefix` `shift+t` | Rename tab |
| `prefix` `p` | Previous tab |
| `prefix` `n` | Next tab |
| `prefix` `1`..`9` | Switch to tab N |
| `prefix` `shift+x` | Close tab |

## Panes

| Keys | Action |
|---|---|
| `prefix` `v` | Split vertical (side by side) |
| `prefix` `-` | Split horizontal (stacked) |
| `prefix` `h` / `j` / `k` / `l` | Focus pane left / down / up / right |
| `prefix` `tab` | Cycle to next pane |
| `prefix` `shift+tab` | Cycle to previous pane |
| `prefix` `z` | Zoom (fullscreen) the pane |
| `prefix` `r` | Resize mode |
| `prefix` `x` | Close pane |
| `prefix` `shift+p` | Rename pane |
| `prefix` `e` | Edit scrollback in `$EDITOR` |

## Navigate mode

Opened with `prefix` `g`. These plain keys apply only while it is open.

| Keys | Action |
|---|---|
| `up` / `down` | Move between workspaces |
| `h` / `j` / `k` / `l` | Focus pane left / down / up / right |
| `left` / `right` | Always focus pane left / right |

## My custom bindings

From `~/.config/herdr/config.toml` (herdr-file-viewer plugin):

| Keys | Action |
|---|---|
| `prefix` `f` | Open file viewer in a split |
| `prefix` `shift+f` | Open file viewer in a new tab |

## Unbound by default (available to set)

These actions exist but have no key until you assign one under `[keys]`:

| Action | Example binding |
|---|---|
| `previous_workspace` / `next_workspace` | |
| `switch_workspace` | `prefix+shift+1..9` |
| `previous_agent` / `next_agent` | |
| `focus_agent` | `prefix+alt+1..9` |
| `open_worktree` / `remove_worktree` | |
| `move_tab_previous` / `move_tab_next` | `alt+shift+left` / `alt+shift+right` |
| `last_pane` | `prefix+tab` (toggle back and forth) |
| `resize_pane_left` / `down` / `up` / `right` | `ctrl+shift+alt+left` etc. |

## Customizing

Action bindings go in `[keys]`; custom commands use `[[keys.command]]`:

```toml
[keys]
prefix = "ctrl+b"
last_pane = "prefix+tab"

[[keys.command]]
key = "prefix+alt+g"
type = "popup"          # or "shell" (background) / "pane" (temp pane)
command = "lazygit"
width = "80%"
height = "80%"
```

- `prefix+x` requires the prefix; `ctrl+alt+x` is a direct shortcut.
- Most reliable direct bindings: `ctrl+letter`, function keys.
  `alt+...`, `cmd`, and modified punctuation depend on the terminal.
- Apply changes with `prefix` `shift+r` or `herdr server reload-config`.
- `herdr config reset-keys` backs up config.toml and removes custom bindings.

## herdr-file-viewer keys (inside the viewer)

Most used; full list in the plugin's `docs/keys.md` and
[herdr-configuration-notes.md](../herdr-configuration-notes.md).

| Key | Action |
|---|---|
| `j` / `k`, `h` / `l` | Move tree cursor / collapse, expand (scroll when content focused) |
| `Tab` | Move focus between tree and content |
| `Enter` / `z` / `Z` | Open file zoomed / toggle zoom / fullscreen the herdr pane |
| `f` | Fuzzy go-to-file |
| `/`, `n` / `N` | Search in file, next / previous match |
| `:` | Go to line |
| `]` / `[` | Next / previous changed file |
| `c` / `d` / `b` | Changed-only / git-status mode / toggle diff baseline |
| `v` / `D` | Cycle view mode / cycle diff presentation |
| `w` | Toggle line wrap |
| `e` | Open in `$EDITOR` |
| `y` / `Y` | Copy relative / absolute path |
| `L` | Line-select mode (copy `file:line` refs or content) |
| `p` | Pin preview |
| `i` / `.` | Toggle gitignored / hidden files |
| `?` | Help |
| `q` / `Esc` | Back out / close viewer |
