# Herdr Configuration Notes

Running notes on configuring herdr and its plugins. Install steps live in
[`herdr-macos-setup.md`](./herdr-macos-setup.md) — this file covers behavior,
diagnosis, and the knobs worth knowing.

## Why the file viewer shows no git diffs

**Diagnosis: untracked files have no diff to show.** This is not a herdr config
problem and does not need another plugin.

`herdr-file-viewer` renders diffs by shelling out to the system `git` CLI and
piping the result to `delta`. Git can only produce a diff against a **baseline**
— a previous version of the file. An untracked file (`??`) has never been
committed, so there is no baseline, so `git diff` emits nothing and `delta` is
never invoked. The viewer correctly falls back to showing file content.

Check with:

```bash
git status --short
```

| Marker | Meaning | Diff shown? |
|---|---|---|
| `M` | tracked, modified | **yes** |
| `A` | added / intent-to-add | **yes** (all additions) |
| `D` | deleted | **yes** |
| `??` | **untracked** | **no** — nothing to compare against |

If every line is `??`, that is the whole explanation.

### Fix: `git add -N`

`-N` (`--intent-to-add`) registers the path with git at zero length without
staging its contents. The file flips `??` → `A` and diffs appear immediately as
all-additions:

```bash
git add -N path/to/file        # one file
git add -N .                   # everything untracked
```

Non-destructive and reversible — `git reset -- path/to/file` puts it back to
`??`. Preferred over committing just to see a diff.

**Verified on this machine (2026-09-15):** with all four changed paths at `??`,
the viewer showed no diffs. After `git add -N` on one file it became `A`, and
both `git diff` (worktree vs index, what `d` mode uses) and `git diff HEAD`
(what `c`/`b` use) produced 63 lines, which `delta` rendered in full color. The
tree was then reset back to `??`.

### It is *not* your gitconfig

Installing `git-delta` often comes with advice to set `[core] pager = delta` in
`~/.gitconfig`. That is irrelevant here. The viewer feeds content to renderers
directly on **stdin** and never goes through git's pager, so global git config
does not affect it either way.

## The two config.toml files

These are distinct and easy to conflate:

| File | Owns |
|---|---|
| `~/.config/herdr/config.toml` | **herdr itself** — keybindings, UI, toasts |
| `~/.config/herdr/plugins/config/herdr-file-viewer/config.toml` | **the plugin** — renderers, view defaults |

The plugin file **does not exist by default, and does not need to.** Every key
has a default, including `changed_file_view = "diff"` — changed files are
already diff-first. Only create it to override something:

```bash
cp ~/.config/herdr/plugins/github/herdr-file-viewer-*/config.example.toml \
   "$(herdr plugin config-dir herdr-file-viewer)/config.toml"
```

(`herdr plugin config-dir herdr-file-viewer` prints the destination;
`herdr plugin list` shows the installed source folder and its pinned commit.)

Renderer overrides are **top-level keys**, not a table:

```toml
markdown = "glow -s dark -w 0 -"
diff     = "delta"                  # defaults: glow / delta / bat
syntax   = "bat --color=always --style=numbers --paging=never --file-name={name} -"

changed_file_view = "diff"          # "content" to start changed files in normal view
```

A custom renderer must read **stdin** (hence glow's and bat's trailing `-`).
Setting a key replaces the whole command; flags are not merged.

## Renderers

Rendering is delegated to external CLIs — all optional, all installed here:

| View | Renderer | Install |
|---|---|---|
| Markdown | `glow` | `brew install glow` |
| Diffs | `delta` | `brew install git-delta` |
| Syntax | `bat` | `brew install bat` |

If one is missing the viewer degrades to plain text and names the missing
capability in the content pane — it never crashes or blanks. **So "no diff" with
no notice means no diff existed; "no diff" with a notice means delta is
missing.** That distinction is the fastest way to tell the two cases apart.

## Diff and git keys

| Key | Action |
|---|---|
| `v` | Cycle view — override the automatic choice (e.g. changed markdown's raw source) |
| `D` | Cycle diff presentation — delta unified → side-by-side → plain `git diff` |
| `d` | Git-status mode — filter to working-tree status, force working-tree diffs |
| `b` | Flip diff baseline — base branch (merge-base) ⇄ `HEAD`. Used by `c` and normal diffs; while `d` is on, content stays working-tree |
| `c` | Changed-files-only filter, against the active baseline |
| `]` / `[` | Jump to next / previous changed file |
| `p` | Pin a frozen snapshot beside the file you keep browsing |
| `z` / `Z` | Zoom content pane / full-screen the herdr pane |

### Reviewing a batch of Claude edits

1. `git add -N .` — give untracked files a baseline so diffs exist.
2. `prefix+f` — open the viewer.
3. `d` — git-status mode: tree shows only changed files, content forced to
   working-tree diffs.
4. `]` / `[` — walk the changed files one at a time.
5. `D` — side-by-side when a change is dense enough to warrant it.

For reviewing a whole branch rather than uncommitted work, use `c` with `b` set
to merge-base instead of `d`.

## Environment

Verified 2026-09-15: herdr 0.9.0 (Homebrew), `herdr-file-viewer` installed from
`smarzban/herdr-file-viewer`, with `glow`, `delta`, and `bat` all on `PATH` at
`/opt/homebrew/bin`.
