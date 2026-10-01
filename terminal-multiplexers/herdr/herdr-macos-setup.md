# Installing and Setting Up Herdr on macOS

Herdr is a Rust-based, agent-aware terminal multiplexer. Single ~10MB binary,
zero dependencies. ([herdr.dev](https://herdr.dev) ·
[GitHub](https://github.com/herdrdev/herdr))

## Install

You already have Homebrew, so use it:

```bash
brew install herdr
```

Alternative (no Homebrew required): the official install script, which also
works on Linux:

```bash
curl -fsSL https://herdr.dev/install.sh | sh
```

## Verify

```bash
herdr --version
herdr
```

If your shell can't find `herdr` after the curl install, restart your
terminal or make sure the install directory is on your `PATH` (Homebrew
handles this automatically).

## First Run

Just launch it:

```bash
herdr
```

Herdr opens with a single pane in your current directory. It's mouse-first —
click panes, drag borders, split/switch via right-click menus — but it also
uses tmux-style prefix keybindings if you prefer the keyboard.

## Config File

- Location: `~/.config/herdr/config.toml`
- Generate the full default config to edit from:

```bash
herdr --default-config > ~/.config/herdr/config.toml
```

## Default Keybindings

Prefix key: `ctrl+b` (same as tmux default).

| Action | Binding |
|---|---|
| New tab | `prefix` `c` |
| Next tab | `prefix` `n` |
| Previous tab | `prefix` `p` |
| Split pane horizontally | `prefix` `-` |
| Focus pane left | `prefix` `h` |
| Show all keybindings | `prefix` `?` |

Panes persist across detach/reattach, same mental model as tmux/screen.

## Plugins

### herdr-file-viewer

Adds a file viewer pane/tab, rendering markdown with
[glow](https://github.com/charmbracelet/glow), diffs with
[git-delta](https://github.com/dandavison/delta), and other files with
[bat](https://github.com/sharkdp/bat).
([GitHub](https://github.com/smarzban/herdr-file-viewer))

Install the plugin and its optional rendering dependencies:

```bash
herdr plugin install smarzban/herdr-file-viewer
brew install glow git-delta bat
```

Then wire up keybindings in `~/.config/herdr/config.toml`:

```toml
[[keys.command]]
key = "prefix+f"
type = "plugin_action"
command = "herdr-file-viewer.open-file-viewer"
description = "open file viewer in split"

[[keys.command]]
key = "prefix+shift+f"
type = "plugin_action"
command = "herdr-file-viewer.open-file-viewer-tab"
description = "open file viewer in tab"
```

`prefix+f` opens the file viewer in a split; `prefix+shift+f` opens it in a
new tab.

See [`herdr-configuration-notes.md`](./herdr-configuration-notes.md) for
renderer/diff configuration, the git-review keybindings, and why untracked
files show no diffs.

## Agent Skill

Herdr ships a skill file that teaches a coding agent to drive Herdr from
inside a Herdr-managed pane — inspecting workspaces/tabs/panes, splitting
panes, reading pane output, waiting on servers or tests, and starting helper
agents in sibling panes.

```bash
npx skills add herdrdev/herdr --skill herdr -g
```

The org is **`herdrdev`**, not `herderdev`. The wrong spelling 404s, and
`npx skills` reports it as `Authentication failed ... For private repos,
ensure you have access`, which points at credentials rather than the typo.

`-g` installs globally; omit it to install into the current project only.
Installs to `~/.agents/skills/herdr/SKILL.md`, symlinked from
`~/.claude/skills/herdr`.

The skill guards on `HERDR_ENV=1` — outside a Herdr pane the agent stops and
says so. So start the agent inside Herdr:

```bash
herdr
claude
```

Note that `--skill herdr` names a skill that exists only as a released
artifact; the repo's own `.agents/skills/` holds unrelated internal dev
skills (`herdr-pre-release-audit`, `herdr-throwaway-repro`, `triage`). If
Herdr is already installed, `herdr --skill` prints the copy matching your
binary. Manual fallback:
[`skills/herdr/SKILL.md`](https://github.com/herdrdev/herdr/blob/master/skills/herdr/SKILL.md).

Separately, [`herdr.dev/agent-guide.md`](https://herdr.dev/agent-guide.md) is
for an agent *teaching a human* to set up Herdr (local copy:
[`herdr-agent-guide.md`](./herdr-agent-guide.md)) — the skill is for an agent
*operating* Herdr.

[`herdr.dev/llms.txt`](https://herdr.dev/llms.txt) is the LLM-oriented index
of the Herdr docs (links to raw source pages pinned to a release). Local copy,
fetched 2026-09-27 at v0.9.1: [`herdr-llms.txt`](./herdr-llms.txt).

## Videos

- [Herdr: Why Developers Are Replacing Tmux with AI Agents](https://www.youtube.com/watch?v=7W_H9313DHQ)
  — Damian Galarza

See [`terminal-multiplexers.md`](../terminal-multiplexers.md) for more
third-party Herdr videos.

## Why Herdr (context)

Chosen over alternatives (tmux, Screen, dvtm, Byobu, cmux, Superlogical) for
native agent-awareness — it marks panes as working/blocked/idle and notifies
when an agent stops and needs input — and because it runs on **both** macOS
and Linux (unlike cmux, which is macOS-only). See
[`terminal-multiplexers.md`](../terminal-multiplexers.md) for the full
comparison.

## Notes

- License: Apache-2.0.
- Windows install (for reference): `powershell -ExecutionPolicy Bypass -c "irm https://herdr.dev/install.ps1 | iex"`.
- A Linux-specific setup doc will be added separately.
- Working against a remote Herdr host (SSH, `herdr --remote`, saved machines):
  see [`herdr-remote-access.md`](./herdr-remote-access.md).
