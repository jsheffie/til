# Terminal Multiplexers Comparison

Ordered oldest → newest by first release.

> **Sourcing note:** Rows marked _(unverified)_ come from secondary blog coverage that could not be
> confirmed against a primary source. Superlogical in particular is in closed beta with no public
> code, so its architecture claims are the company's own, not independently checked.

## Comparison Table

| Feature | GNU Screen | tmux | dvtm | Byobu | cmux | Herdr | Superlogical |
|---|---|---|---|---|---|---|---|
| **Links** | [gnu.org](https://www.gnu.org/software/screen/) · [git](https://git.savannah.gnu.org/cgit/screen.git) | [GitHub](https://github.com/tmux/tmux) · [wiki](https://github.com/tmux/tmux/wiki) | [brain-dump.org](https://www.brain-dump.org/projects/dvtm/) · [GitHub](https://github.com/martanne/dvtm) | [byobu.org](https://byobu.org/) · [GitHub](https://github.com/dustinkirkland/byobu) | [GitHub](https://github.com/manaflow-ai/cmux) | [herdr.dev](https://herdr.dev) · [GitHub](https://github.com/herdrdev/herdr) | [superlogical.com](https://www.superlogical.com) · [@superlogical](https://x.com/superlogical) |
| **First Release** | 1987 | Nov 20, 2007 | Dec 8, 2007 | 2009 (as screen-profiles, Dec 2008) | Jan 28, 2026 (repo); Feb 12, 2026 (release) | Mar 27, 2026 (repo); Aug 3, 2026 (v0.8.0) | Announced Jul 2026 (closed beta) |
| **Open Source** | Yes (GPL-3.0-or-later) | Yes (ISC) | Yes (MIT/X11) | Yes (GPL-3.0) | GPL-3.0 + commercial option (auto-detect: NOASSERTION) | Yes (Apache-2.0; was AGPL-3.0) | **No** — proprietary; OSS pieces promised |
| **Maintained?** | Yes, slowly (v5.0.2) | Yes, active | **Dormant** — last commit Mar 2021, last release v0.15 (2016) | Yes, active (last push Sep 2026) | Yes, active | Yes, very active | Pre-release |
| **macOS** | Ships as `/usr/bin/screen` but **v4.00.03 from 2006** | Yes (Homebrew; **not** preinstalled) | Source only, no Homebrew formula | Yes (Homebrew v7.19) | **Yes — macOS only** | Yes | Yes (native app) |
| **Linux** | Yes, universal | Yes | Yes (Debian/Ubuntu) | Yes (Ubuntu default) | **No** | Yes (incl. WSL) | Not confirmed |
| **Primary Focus** | Original persistent sessions | Human-centric persistent sessions | Minimal, dwm-style tiling | Status-bar UX layer over tmux/screen | Running multiple AI agents on macOS | AI coding agent runtime & monitoring | Human+AI unified sessions, multi-device |
| **Written In** | C | C | C | Shell/Python wrapper | Swift + AppKit (libghostty) | Rust | Unknown |
| **AI Agent Awareness** | None | None | None | None | **High** | **High** — panes marked working/blocked/idle | Claimed high _(unverified)_ |
| **Agent-waiting notification** | ✗ Generic `monitor` bell, **off by default** | ⚠ `monitor-activity`/`monitor-silence` + hooks, DIY | ✗ | ⚠ Turns backend monitoring **on** by default; no agent concept | ✓ Blue ring on pane, tab lights up, `cmux notify` CLI, Cmd+Shift+U | ✓ **Native** — notifies when agent stops and needs input; sound supported | ✗ Pending |
| **Architecture note** | — | Text-escape sequence parser | — | Wraps tmux (default) or screen | Built on Ghostty's engine | Terminal wrapper + socket API | Binary wire protocol over `libhosty` _(unverified)_ |

## Your Requirement: Bell When an Agent Waits on Input

| Tool | Meets it? | How |
|---|---|---|
| **Herdr** | ✓ **Yes** | Native. Marks panes blocked/idle, notifies on stop, sound support. Runs on macOS **and** Linux. |
| **cmux** | ✓ Yes, but | Native and well-designed — **macOS only**, so it fails your Linux requirement. |
| **Superlogical** | ✗ Not yet | Designed for human+AI work, but closed beta; no notification details published. |
| **tmux** | ⚠ DIY | `monitor-silence` + hooks can approximate it, but you script and maintain it yourself. |
| **Byobu** | ⚠ DIY | Same as tmux underneath; better defaults, still no agent concept. |
| **Screen / dvtm** | ✗ No | Screen's bell is off by default and window-scoped; dvtm is dormant. |

## Recommendation

**Herdr** is the only option that satisfies all your stated constraints:

1. ✓ Native bell/notification when an agent is waiting on input
2. ✓ Runs on **both** macOS and Linux
3. ✓ Purpose-built for Claude Code and similar agents
4. ✓ Open source (Apache-2.0), single Rust binary
5. ✓ Actively developed

**On your lean toward Superlogical:** it's a strong team (Mitchell Hashimoto, of HashiCorp and Ghostty) and the vision fits what you want — but it is **closed beta, proprietary, Linux support unconfirmed, and has no published notification mechanism**. You cannot use it today, and its headline performance claims are unverifiable while the code is private. Worth watching; not worth waiting on.

**cmux** is the closest rival to Herdr on features and is worth a look if you ever work macOS-only — but it cannot cover your Linux machine.

**tmux** stays the safe fallback: universal, battle-tested, and you can hand-roll agent notifications with `monitor-silence` and hooks if you'd rather not adopt a young tool.

## Videos

Third-party videos covering Herdr:

- [herdr is a must use](https://www.youtube.com/watch?v=2CR9tDNAzB0&t=329s) — Academind
- [Herdr in about 6 minutes](https://www.youtube.com/watch?v=qnIu-Xu64H0&t=14s) — Jilles

## Notes & Caveats

- macOS ships an ancient Screen (4.00.03, 2006) and does **not** ship tmux — both need Homebrew for current versions.
- dvtm is effectively abandoned; included for completeness only.
- Screen 5.0.2's exact release date and its status on macOS 26 (Tahoe) could not be confirmed.
- Third-party blog comparisons of these tools are frequently AI-generated and carry wrong dates and star counts; prefer the repos above.
