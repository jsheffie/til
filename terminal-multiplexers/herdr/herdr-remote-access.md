# Running Herdr Against a Remote Machine

How to work with Herdr sessions running on a remote host (here: `omarchy`,
an Arch/Omarchy box on the LAN) from this Mac, while keeping local
keybindings, theme, and clipboard image paste.

Sources: [How to work with Herdr](https://herdr.dev/docs/how-to-work/),
[Persistence and remote access](https://herdr.dev/docs/persistence-remote/),
[Connecting machines](https://herdr.dev/docs/connecting-machines/),
[Session state and restore](https://herdr.dev/docs/session-state/).
Written against Herdr 0.9.1 (2026-09-27).

## TL;DR

Run the Herdr **client on the Mac** and attach to the remote **server** over
SSH. Pick one of:

- `herdr --remote omarchy` - one remote session in a local UI.
- `herdr machine add omarchy ...` then plain `herdr` - Local plus remote
  sessions in one window (recommended for day-to-day).

Before either works cleanly, omarchy needs a one-time upgrade from 0.8.2 to
0.9.x (see [One-time omarchy upgrade](#one-time-omarchy-upgrade)).

## Mental model

Herdr is a background **server** that owns the pane processes, plus one or
more **clients** that render the UI. The question is only where the client
runs:

| | Server runs on | Client (UI) runs on |
|---|---|---|
| `ssh omarchy` then `herdr` | omarchy | omarchy (inside your SSH TTY) |
| `herdr --remote omarchy` | omarchy | Mac |
| `herdr machine add omarchy` + `herdr` | omarchy (and Local) | Mac |

In every case the agents, shells, code, and credentials live on omarchy, and
panes survive the SSH connection dropping.

## The three options

### 1. SSH first, then run herdr remotely (tmux-style)

```bash
ssh omarchy
herdr                             # default session
herdr session attach hyperland    # named session
```

Pros:

- Simplest. No version coupling between Mac and omarchy.
- Works from any SSH client, including a phone.
- Uses omarchy's own config exactly as-is.

Cons:

- Keybindings, theme, and sidebar settings are **omarchy's**, not the Mac's.
  (omarchy's prefix is `ctrl+space`; the Mac uses the default `ctrl+b`.)
- No clipboard image paste: the remote Herdr cannot read the Mac clipboard.
  Screenshots cannot be pasted into Claude Code in a pane.
- UI redraws travel over SSH as terminal output.

### 2. `herdr --remote` (local client, one remote session)

```bash
herdr --remote omarchy                       # default session
herdr --remote omarchy --session hyperland   # named session
```

Pros:

- The UI is drawn by the Mac client: Mac theme, sidebar, menus, copy mode.
- **Mac keybindings by default** (`--remote-keybindings server` to opt out).
- **Clipboard image paste is bridged**: the image is copied to a remote temp
  file and the path is pasted (`ctrl+v`, see
  [herdr_keybindings.md](./herdr_keybindings.md)). This is the screenshot
  workflow for Claude Code on omarchy.
- Herdr manages SSH keepalives and a control socket for connection reuse.

Cons:

- One session per client window. `default` and `hyperland` need two
  terminals (or two attaches in sequence).
- Requires compatible Herdr on both sides (versions need not match once both
  are 0.9.x / endpoint generation 1).
- Local **custom command keybindings are not sent** (they would run on the
  remote). The `prefix+f` / `prefix+shift+f` herdr-file-viewer bindings in the
  Mac config do nothing in remote panes unless the plugin is also installed on
  omarchy.

### 3. Saved SSH machines (local client, many machines in one window)

```bash
herdr machine add omarchy --label omarchy
herdr machine add omarchy --label omarchy-hyperland --remote-session hyperland
herdr                                        # Local + both remote sessions
```

Pros:

- One Herdr window shows Local and every saved remote session in the sidebar,
  with a combined agent list and notifications ("which agent is blocked,
  anywhere").
- Automatic background reconnects after sleep or network loss; one dead
  machine does not affect the others.
- Uses Mac theme, sidebar settings, and keybindings.
- Scriptable from the Mac without a TUI:
  `herdr --machine omarchy agent list`.

Cons:

- **One profile per remote session**, so `default` and `hyperland` are two
  profiles.
- Background connections are non-interactive. Host-key prompts, passphrases,
  installs, or upgrades show as **Attention**; fix them by running
  `herdr --remote omarchy [--session <name>]` interactively once, then
  restarting the client. Load passphrase-protected keys with `ssh-add` first.
- Needs a 0.9.x server on omarchy (`surface_interest` and `health_check`
  capabilities). A 0.8.2 server stays in Attention.
- Clipboard image paste is documented for `herdr --remote`; the docs do not
  explicitly promise it for saved machines. Verify before relying on it, and
  fall back to option 2 for screenshot-heavy work if it does not work.
- Same custom-command caveat as option 2: commands and plugins run on the
  selected server, so omarchy needs its own plugins.

### Which one

| Goal | Use |
|---|---|
| Mac keybindings + screenshot paste into a remote agent | 2 (`--remote`) or 3 |
| Watch agents on Local and omarchy together | 3 (saved machines) |
| Quick check from a phone or a random terminal | 1 (SSH then `herdr`) |
| omarchy not yet upgraded | 1 |

## One-time omarchy upgrade

State on 2026-09-27:

| | Mac | omarchy |
|---|---|---|
| Herdr | 0.9.1 (Homebrew) | 0.8.2 (`/usr/bin/herdr`, AUR package `herdr`) |
| Arch | arm64 | aarch64 |
| Prefix | `ctrl+b` (default) | `ctrl+space` |
| Sessions | - | `default`, `hyperland` (each running an idle Claude Code agent) |
| Claude integration | - | not installed |

Why it matters:

- 0.9.0 introduced "endpoint generation 1". Servers older than that need **one
  final stop** before a 0.9.x client can use them. After that, client and
  server versions can drift without restarts.
- `default` and `hyperland` are **separate servers**, so this happens twice.
- Stopping a server **ends its pane processes**. With no Claude integration on
  omarchy, Herdr cannot auto-resume the Claude sessions (it restores layout and
  cwd only).

### Procedure

1. **Upgrade the package on omarchy with yay, not Herdr's installer.**

   ```bash
   ssh omarchy
   yay -S herdr-bin     # 0.9.1, supports aarch64, replaces the `herdr` source package
   herdr --version
   ```

   Do not let `herdr --remote` install its own copy. It would go to
   `~/.local/bin/herdr`, which is **behind** `/usr/bin` on omarchy's `PATH`, so
   a plain `ssh omarchy; herdr` would keep running the old 0.8.2 binary. Keep
   one pacman-owned binary.

2. **Note the Claude sessions** you care about (the running servers are still
   0.8.2 at this point):

   ```bash
   herdr agent list
   herdr --session hyperland agent list
   ```

   Both agents were idle, so the cheap path is to let them stop and resume by
   hand afterwards.

3. **Replace each server.** Pick one:

   - **Stop and restart** (predictable):

     ```bash
     herdr session stop hyperland
     herdr server stop                # default session
     ```

     Then attach from the Mac (next step). Layout and cwd come back; resume
     Claude in each pane with `claude --resume` (or `claude --continue`) in
     `~/workspace` and `~/workspace/hyperland`.

   - **Live handoff** (experimental, keeps processes alive if it works). From
     the Mac:

     ```bash
     herdr --remote omarchy --handoff
     herdr --remote omarchy --session hyperland --handoff
     ```

   If you just run `herdr --remote omarchy` against a 0.8.2 server, it asks
   before stopping it. The default answer is **No**.

4. **Install the Claude integration on omarchy** so future server restarts
   resume Claude conversations automatically:

   ```bash
   ssh omarchy herdr integration install claude
   ssh omarchy herdr integration status
   ```

5. **Attach from the Mac** with option 2 or 3 above. For saved machines, run
   `herdr machine list` afterwards to confirm both profiles.

## Keybinding alignment

With options 2 and 3 the Mac keybindings apply, so the remote prefix is
`ctrl+b`. With option 1 it is omarchy's `ctrl+space`. To have one prefix
everywhere, set the same `[keys] prefix` in both configs (Mac:
`~/.config/herdr/config.toml`), then use the `reload config` action in the UI.

Nested Herdr (running `herdr` inside a pane of another Herdr) will fight over
the prefix. Prefer attaching from the Mac over SSH-ing to omarchy from inside a
local Herdr pane and starting `herdr` there.

## SSH notes

`~/.ssh/config` already has:

```text
Host omarchy omarchy.local
    HostKeyAlias omarchy
    User jds
    AddressFamily inet
```

That is all `herdr --remote omarchy` needs. Herdr layers its own keepalive
settings on top unless the host already sets `ServerAliveInterval`. Set
`[remote].manage_ssh_config = false` in the Mac config to use plain `ssh`.

If an attach fails, check plain `ssh omarchy` first, then retry.

## Troubleshooting

- `herdr status` on either side shows client/server versions, protocol, and
  `compatible:`.
- Logs: `~/.config/herdr/herdr-client.log` (Mac) and
  `~/.config/herdr/herdr-server.log` (omarchy).
- A machine shows **Attention**: run the standalone
  `herdr --remote omarchy [--session hyperland]` in a terminal, answer the
  prompts, restart the client.
- Cached (dimmed) workspaces after a network drop are stale; input is disabled
  until the reconnect completes.
