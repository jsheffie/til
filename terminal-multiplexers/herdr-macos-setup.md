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

## Why Herdr (context)

Chosen over alternatives (tmux, Screen, dvtm, Byobu, cmux, Superlogical) for
native agent-awareness — it marks panes as working/blocked/idle and notifies
when an agent stops and needs input — and because it runs on **both** macOS
and Linux (unlike cmux, which is macOS-only). See
[`terminal-multiplexers.md`](./terminal-multiplexers.md) for the full
comparison.

## Notes

- License: Apache-2.0.
- Windows install (for reference): `powershell -ExecutionPolicy Bypass -c "irm https://herdr.dev/install.ps1 | iex"`.
- A Linux-specific setup doc will be added separately.
