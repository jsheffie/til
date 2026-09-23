# Diff Tools Comparison

Terminal and desktop diff tooling for reviewing coding-agent changes in Herdr, with GitHub as the forge.
Ordered oldest → newest by first release.

> **Sourcing note:** Repo dates, licenses, languages and latest releases were pulled from the GitHub API on
> Sep 17, 2026. Local versions were checked on this Mac. Cells marked _(not confirmed)_ could not be verified
> against a primary source. **There are two projects called `hunk`:** the one people mean, and the one
> `brew install hunk` gives you, is [modem-dev/hunk](https://github.com/modem-dev/hunk) (TypeScript, since
> Mar 2026). A separate, unrelated [wmarquardt/hunk](https://github.com/wmarquardt/hunk) (Go, Sep 2026,
> stages hunks) appeared two weeks ago and is listed in the notes only.

## Comparison Table

| Feature | diff / patch | vimdiff / nvim -d | git diff / apply | GitHub Desktop | lazygit | delta | difftastic | gh CLI | hunk | herdr-file-viewer | herdr-reviewr |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Links** | [gnu.org diffutils](https://www.gnu.org/software/diffutils/) · [GNU patch](https://savannah.gnu.org/projects/patch/) | [:help diff](https://neovim.io/doc/user/diff.html) · [GitHub](https://github.com/neovim/neovim) | [git-diff](https://git-scm.com/docs/git-diff) · [git-apply](https://git-scm.com/docs/git-apply) | [desktop.github.com](https://desktop.github.com) · [GitHub](https://github.com/desktop/desktop) · [Linux fork](https://github.com/shiftkey/desktop) | [GitHub](https://github.com/jesseduffield/lazygit) | [docs](https://dandavison.github.io/delta/) · [GitHub](https://github.com/dandavison/delta) | [site](https://difftastic.wilfred.me.uk/) · [GitHub](https://github.com/Wilfred/difftastic) | [cli.github.com](https://cli.github.com) · [GitHub](https://github.com/cli/cli) | [hunk.dev](https://hunk.dev) · [GitHub](https://github.com/modem-dev/hunk) | [GitHub](https://github.com/smarzban/herdr-file-viewer) · [config docs](https://github.com/smarzban/herdr-file-viewer/blob/main/docs/configuration.md) | [GitHub](https://github.com/persiyanov/herdr-reviewr) |
| **First Release** | diff: 1974 (Unix v5); patch: 1985 (Larry Wall) | Vim 6.0 diff mode: Sep 2001; Neovim: Jan 2014 (repo) | Apr 2005 | GitHub for Mac: Jun 2011; Electron rewrite open-sourced May 2017, 1.0 Sep 2017 | May 2018 (repo); Aug 2018 (first tagged release) | Jun 24, 2019 (repo); 0.0.1 Jul 16, 2019 | Dec 2018 (repo); 0.1.0 Jan 3, 2020 (crates.io) | Oct 2019 (repo); beta Feb 2020, 1.0 Sep 2020 | Mar 17, 2026 (repo); v0.4.0 Mar 22, 2026 | Jun 18, 2026 (repo); v1.0.0 Jun 22, 2026 | Jun 26, 2026 (repo and v0.1.0) |
| **Open Source** | Yes (GNU: GPL-3.0-or-later; Apple diff: BSD) | Yes (Vim license; Neovim Apache-2.0) | Yes (GPL-2.0) | Yes (MIT, since 2017) | Yes (MIT) | Yes (MIT) | Yes (MIT; tree-sitter grammars mixed MIT/Apache) | Yes (MIT) | Yes (MIT) | Yes (MIT) | Yes (MIT) |
| **Maintained?** | Yes, slowly (diffutils 3.12) | Yes, very active (NVIM 0.12.5 installed) | Yes, very active | Yes, active (3.6.6; 3.6.7-beta1 Sep 16, 2026) | Yes, very active (v0.65.1 Sep 13, 2026) | Yes, active (0.19.2 Mar 2026; push Sep 15, 2026) | Yes, active (0.70.0 Aug 7, 2026) | Yes, very active (v2.101.0 Sep 15, 2026) | Yes, very active (v0.22.0 Sep 10, 2026; 71 releases in 6 months) | Yes, very active (v1.17.0 Sep 16, 2026) | Yes, very active (v0.38.0 Sep 16, 2026) |
| **macOS** | Ships **Apple diff (FreeBSD-based)** and Apple patch 2.0, **not GNU**; `brew install diffutils` for GNU | Yes (vim preinstalled; nvim via Homebrew) | Yes (Apple Git 2.39.5 via Xcode CLT; newer via Homebrew) | **Yes** (cask `github`; installed here) | Yes (Homebrew) | Yes (`brew install git-delta`; installed 0.19.2) | Yes (Homebrew) | Yes (Homebrew; installed 2.100.0) | Yes (`brew install hunk`, curl, npm, mise, Nix) | Yes (needs Herdr) | Yes (needs Herdr for Send) |
| **Linux** | Yes, universal (GNU) | Yes | Yes | **No official build.** Community fork `shiftkey/desktop`: last release Feb 2025, last push May 2025 | Yes | Yes | Yes (and Windows) | Yes (and Windows) | Yes (and Windows) | Yes | Yes (**no** Windows) |
| **Primary Focus** | Line-oriented text diffs and applying them; the unified-diff format everything else speaks | Editing both sides of a diff; 2- and 3-way merges | Diffing against any baseline: index, HEAD, branch, merge-base | GUI commit/push/PR flow with a visual diff of working tree and history | Full git TUI: staging, rebasing, branches; the diff is one panel | Syntax-highlighted pager for git, diff, grep output | Structural (syntax-tree) diffs that ignore reformatting noise; 30+ languages | GitHub from the terminal: PRs, issues, checks, releases | Reading agent-authored changesets: many files, one stream | Read-only, git-aware tree and content pane inside Herdr; diff-first for changed files | Code-review sidebar: comment on an agent's diff and send it back to the agent |
| **Written In** | C | C + Lua / Vim script | C (+ shell, Perl) | TypeScript (Electron) | Go | Rust | Rust | Go | TypeScript (OpenTUI, Pierre diffs); standalone binary, no Node needed | Rust | Rust (ratatui) |
| **AI Agent Awareness** | None | None (plugins only) | None | None for review | None | None | None | ⚠ `gh copilot` extension; nothing diff-specific | **High** — built for agent diffs; `hunk skill path` hands your agent a skill file; inline agent annotations | ⚠ Medium — Herdr-native, sits beside agent panes, but no agent concept of its own | **High** — comments go straight into the agent's input; "last turn" diff scope |
| **Runs in a Herdr pane?** | ✓ Plain text, anywhere | ✓ | ✓ It is what herdr-file-viewer shells out to | ✗ Separate window; not a terminal app | ✓ TUI | ✓ **Already the diff renderer inside herdr-file-viewer** | ⚠ Yes as a command; **no** as the file-viewer `diff` renderer (needs two files, rejects `--line-numbers`) | ✓ | ✓ TUI; `hunk diff --watch` reloads as the agent edits | ✓ **Native plugin** — already installed | ✓ **Native plugin**; standalone binary works minus Send |
| **Side-by-side** | ⚠ `diff -y` / `sdiff`, no color | ✓ Native, unchanged regions folded | ✗ Pager's job; `--word-diff` only | ✓ Split toggle, hide whitespace, expand context | ⚠ Via pager config (`delta --paging=never`) | ✓ `-s`, line numbers, word-level emphasis | ✓ Default when the terminal is wide enough | ✗ Emits unified diff; pipe to delta | ✓ Split / unified / auto-responsive | ✓ Via delta; `D` cycles unified → side-by-side → plain | _(not confirmed)_ |
| **Stage hunks / write a patch** | ✓ **This is the patch tooling:** `diff -u` makes, `patch -p1` applies; no git needed | ⚠ `do` / `dp` move hunks between buffers; git staging via plugins | ✓ `add -p`, `apply`, `format-patch` / `am`, `add -N` | ✓ Line-level partial commits by clicking; no patch export | ✓ Stage by file, hunk or line; build custom patches from commits | ✗ Display only; `interactive.diffFilter` colors `git add -p` | ✗ Output is for humans; cannot produce a patch | ⚠ `pr diff --patch` gives `git am` input; `pr checkout` | ✗ Read-only review | ✗ Read-only; untracked files need `git add -N` to show a diff | ✗ Review, not staging |
| **GitHub PR integration** | ✗ But `gh pr diff` output is unified diff you can `patch` | ✗ Plugins (octo.nvim) | ⚠ `git diff origin/main...` after fetch; no PR metadata | ✓ Check out PR branches, see CI status, open PR in browser; review happens on github.com | ⚠ Opens a create-PR page in the browser; no PR review | ⚠ `gh pr diff 123 \| delta`; commit hyperlinks | ✗ Use `git difftool` after checkout | ✓ **Native** — `pr diff`, `view`, `checks`, `review`, `comment` | ⚠ `gh pr diff 123 \| hunk patch -`; no PR metadata | ✗ `b` flips baseline to merge-base, which approximates the PR diff | ✓ Read-only PR tab: state, checks, description, comments — reads via `gh` (also GitLab, Azure DevOps); never posts |
| **Architecture note** | stdout text; unified diff is the lingua franca | `git difftool -t vimdiff` / `git mergetool`; edits the files in place | Plumbing; every tool here wraps it | Electron app wrapping git (dugite) | TUI over the git CLI; delta and difftastic pluggable | stdin → stdout filter; `core.pager` | `GIT_EXTERNAL_DIFF=difft` or `git difftool`; not a pager | REST/GraphQL API client; text output | TUI: `hunk diff`, `show`, `log`, `patch -` (stdin) | Shells out to git, pipes to delta / glow / bat; custom `diff` renderer must accept `--line-numbers` | ratatui TUI; `]` walks hunks, `a` marks reviewed, `c` comments, `s` sends to agent |

## Your Requirement: Review an Agent's Diff Inside Herdr, With GitHub as the Forge

| Tool | Meets it? | How |
|---|---|---|
| **herdr-reviewr** | ✓ **Yes** | Herdr-native. Shows the agent's diff, takes line comments, sends them into the agent's input. PR tab reads state, checks and comments through `gh`. |
| **hunk** | ✓ **Yes** | Best reader for a big multi-file changeset. Run it in a pane next to the agent with `--watch`. No staging, no PR metadata. |
| **delta + herdr-file-viewer** | ✓ Already have | Installed and wired. Covers "glance at what changed" with `D` for side-by-side. Keep it. |
| **gh CLI** | ✓ The glue | `gh pr diff \| delta` or `\| hunk patch -` today; it is also what herdr-reviewr's PR tab reads through. |
| **GitHub Desktop** | ⚠ Outside Herdr | Still the easiest line-level partial commit and a good final visual pass. Separate window, no Linux build. |
| **lazygit** | ⚠ Overlaps | Best terminal hunk-staging if you want GitHub Desktop's partial commits without leaving Herdr. Not agent-aware. |
| **difftastic** | ⚠ Niche | Worth it when an agent reformats while it refactors. Cannot feed herdr-file-viewer or make patches. |
| **vimdiff / nvim -d** | ⚠ Merges | Reach for it as `git mergetool`, not as a review tool. |
| **diff / patch / git** | ✓ Plumbing | Always there. Every tool above produces or consumes their unified-diff format. |

## Recommendation

**Keep delta, add hunk and herdr-reviewr, keep GitHub Desktop for what it is good at:**

1. ✓ **delta** stays as the renderer inside herdr-file-viewer — nothing to change
2. ✓ **hunk** (`brew install hunk`) in its own pane for reading a large agent changeset; `hunk diff --watch` follows the agent live
3. ✓ **herdr-reviewr** (`herdr plugin install persiyanov/herdr-reviewr`) when you want to comment on the diff and push feedback back to the agent, or check PR state without leaving Herdr
4. ✓ **GitHub Desktop** stays for line-level partial commits and the final visual pass before pushing
5. ✓ **gh** is already installed and ties the PR side together

**On hunk and staging:** the popular hunk is read-only. If you want to stage hunks in the terminal the way you
click lines in GitHub Desktop, that is **lazygit**, or `git add -p` with `interactive.diffFilter = delta --color-only`
so the prompts are colored. The newer [wmarquardt/hunk](https://github.com/wmarquardt/hunk) does stage hunks but is
two weeks old with four stars; watch it, do not depend on it yet.

**On difftastic:** it is the only tool here that understands syntax, so a reformat-plus-refactor shows as a small
diff instead of a wall of red and green. It is a `git difftool`, not a pager, and it cannot be dropped into
herdr-file-viewer's `diff` setting because that setting expects a stdin filter that accepts `--line-numbers`.

**On GitHub Desktop:** you have used it forever and nothing here replaces its line-level partial commit UI. Its
limits are that it lives outside Herdr and has no official Linux build. The community Linux fork has not shipped
since Feb 2025.

## Command-Line Diff and Patch Tooling

The plumbing under everything above. Worth knowing because every tool here either emits or consumes this format.

```sh
# Classic diff/patch, no git required
diff -u old.txt new.txt > change.patch      # unified diff; -r for directories, -y for side-by-side
patch -p1 < change.patch                    # apply; -R to reverse, --dry-run to test

# git equivalents
git diff                                     # working tree vs index (what herdr-file-viewer's d mode shows)
git diff HEAD                                # working tree vs last commit
git diff main...                             # branch vs merge-base with main (what b flips to)
git diff --stat                              # files and line counts only
git diff --word-diff                         # word-level instead of line-level
git add -N .                                 # give untracked files a baseline so diffs exist
git add -p                                   # stage hunk by hunk
git diff > change.patch; git apply change.patch
git format-patch -1 HEAD; git am 0001-*.patch  # patches that carry commit metadata

# Coloring and structure
git diff | delta -s                          # side-by-side with syntax highlighting
git config --global interactive.diffFilter "delta --color-only"   # colors git add -p
GIT_EXTERNAL_DIFF=difft git diff             # structural diff, one-off
git difftool -t vimdiff                      # edit both sides

# GitHub PRs from the terminal
gh pr diff 123 | delta                       # PR diff, colored
gh pr diff 123 | hunk patch -                # PR diff in hunk
gh pr diff 123 --patch | git am              # apply a PR's commits locally
gh pr checkout 123; gh pr checks; gh pr view --comments
```

## Notes & Caveats

- Two projects are called `hunk`. `brew install hunk` installs `modem-dev/hunk` (0.22.0). `wmarquardt/hunk` is a separate Go project created Sep 3, 2026 that stages hunks; it is not on Homebrew.
- Current macOS ships Apple's FreeBSD-derived `diff` and Apple `patch` 2.0, not GNU diffutils. Flags like `--color` differ; `brew install diffutils` for GNU.
- Setting `core.pager = delta` in gitconfig neither helps nor hurts herdr-file-viewer; it feeds renderers on stdin and never goes through git's pager.
- herdr-reviewr's side-by-side support and its exact first-release feature set were not confirmed against its docs.
- GitHub Desktop dates before the 2016 repo (GitHub for Mac 2011, GitHub Desktop 2015) are from memory of the product history, not the API.
- diff-so-fancy (Perl, 2016, still maintained) is delta's predecessor and is omitted from the table; delta covers everything it does.
- Third-party blog comparisons of these tools are frequently AI-generated and carry wrong dates and star counts; prefer the repos linked above.
