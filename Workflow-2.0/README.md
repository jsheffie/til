# Workflow 2.0: terminal-only code review

Goal: do the whole code review loop without leaving the terminal emulator.

The phases below are tool-agnostic on purpose. Tools will get swapped in and out
while I look for a flow I like; the phases should stay the same.

## Phases

```
workspace -> triage -> fetch -> diff -> explore -> review -> follow up
```

| # | Phase | What happens here | Done when |
|---|---|---|---|
| 0 | **Workspace** | The layer everything runs in: terminal emulator plus a multiplexer that holds a pane per repo or task and survives detach. Not really a step, it is always there. | A pane exists for the repo I am reviewing |
| 1 | **Triage** | See what needs my attention: PRs assigned to me, review requests, CI status, notifications. Pick one. | I have chosen a PR |
| 2 | **Fetch** | Get the PR branch onto my machine so local tools can see it. | PR branch is checked out (or a worktree exists for it) |
| 3 | **Diff** | Read the change itself: changed files, hunks, commits. | I understand what changed |
| 4 | **Explore** | Leave the diff and read the surrounding code on the PR branch: callers, tests, history, blame. Run tests if needed. | I understand why it changed and what it touches |
| 5 | **Review** | Leave line comments and suggestions, write the summary, approve / request changes / comment. | Review is submitted on GitHub |
| 6 | **Follow up** | Watch for replies, re-review after new pushes, merge, clean up the local branch. | PR is merged or closed and the branch is gone locally |

Phases 3 and 4 loop. Phases 5 and 6 loop until merge.

## Current tooling

| # | Phase | Tool | How I use it | Notes / gaps |
|---|---|---|---|---|
| 0 | Workspace | terminal emulator: _TBD_ | | Fill in once I settle on one |
| 0 | Workspace | [herdr](../terminal-multiplexers/herdr/) | One workspace per repo, panes for shell, agent, editor | Agent-aware sidebar, `prefix` `?` for keys |
| 1 | Triage | [gh dash](https://github.com/dlvhdr/gh-dash) | List PRs and issues across repos, filter to "needs my review" | Also `gh pr list`, `gh pr status` |
| 2 | Fetch | gh dash keybind, or `gh pr checkout <n>` | Check the PR branch out locally | Try `git worktree` so main stays untouched |
| 2 | Fetch | [lazygit](https://github.com/jesseduffield/lazygit) | Checkout a remote branch or create a worktree from the branches panel | Local git only, knows nothing about PRs |
| 3 | Diff | [octo.nvim](../neovim/octo-nvim.md) `:Octo review start` | Changed-files panel plus two-way diff inside Neovim | Can only comment on lines inside a hunk |
| 4 | Explore | Neovim on the checked-out branch | Telescope, LSP go-to-definition, gitsigns | Blame and history: see [neovim-GitLense-options.md](../neovim/neovim-GitLense-options.md) |
| 4 | Explore | lazygit | Commit history, per-commit diffs, file history, interactive rebase when fixing the branch myself | Run in a herdr pane, or float it in Neovim with lazygit.nvim / snacks.nvim `lazygit` |
| 5 | Review | octo.nvim | `Space c a` line comment, `Space s a` suggestion, `:Octo review submit` | `Ctrl-a` approve, `Ctrl-r` request changes |
| 6 | Follow up | gh dash, `gh pr checks`, `gh pr merge` | Watch CI, re-review, merge | Notifications: nothing terminal-side yet |
| 6 | Follow up | lazygit | Delete merged local branches, prune worktrees, pull after merge | |

lazygit is a local git cockpit, not a GitHub client. It never replaces gh dash (Triage) or
octo (Review); it sits beside them in Fetch, Explore and Follow up.

### Current path, end to end

```
herdr  ->  gh dash  ->  gh pr checkout  ->  nvim + Octo review  ->  Octo review submit  ->  gh dash
```

## Things to try

Alternatives per phase, so swapping is a one-row change in the table above.
Most of the tool names come from a Grok conversation (see [References](#references)) and
are not verified yet; check each repo before installing.

| Phase | Alternatives |
|---|---|
| Triage | `gh` CLI aliases, [gh-notify](https://github.com/meiji163/gh-notify) for notifications, octo.nvim `:Octo pr list` or snacks.nvim picker (skip gh dash entirely), or one of the dashboard TUIs below |
| Fetch | `git worktree add` per PR, `gh pr checkout` from inside octo (`:Octo pr checkout`) |
| Diff | [diffview.nvim](https://github.com/sindrets/diffview.nvim) `:DiffviewOpen main...HEAD`, [delta](https://github.com/dandavison/delta) in the shell, lazygit diff view, `gh pr diff`, gitsigns `change_base` to the PR target branch |
| Explore | neogit or lazygit for history, gitsigns `current_line_blame` for inline blame |
| Review | `gh pr review --approve / --request-changes / --comment` for quick ones with no line comments, or one of the review TUIs / Neovim reviewers below |
| Follow up | `gh pr checks --watch`, `gh pr merge --squash --delete-branch`, herdr notifications, prtop |

### Triage: dashboard TUIs (gh dash alternatives)

| Tool | Angle |
|---|---|
| [gh dash](https://github.com/dlvhdr/gh-dash) | Current. Configurable sections, gh extension |
| ghdash | Rust/ratatui. Orgs, all open PRs, review inbox, search, auto-refresh. More "inbox across repos" than configurable sections |
| prtop | Small live monitor of PRs I author or review, with notifications. Also a Follow up candidate |
| gitpane | Multi-repo workspace TUI, local status plus PRs/issues. Complements lazygit |
| github-pr-attention | Focused "PRs that need me" inbox. Comment, approve, request changes, squash merge from the list |

### Review: standalone TUIs (do the review outside Neovim)

These cover Diff and Review in one tool, no checkout needed.

| Tool | Angle |
|---|---|
| gh-prism | gh extension. Description, commits, files, conversation, highlighted diffs, inline comments and suggestions, submit, merge. `gh extension install kawarimidoll/gh-prism`, then `gh prism 123`. Grok's "try this first" pick |
| tuicr | Vim motions, GitHub-style continuous diff, line and range comments, submits to GitHub or GitLab. Also works on local diffs |
| prtui | Modal, vim-ish, GitHub PRs and GitLab MRs. Can review local uncommitted diffs |
| prr | Writes the PR to a review file I edit in Neovim, then submits. Pairs well with worktrees |

### Review: Neovim plugins (octo.nvim alternatives)

| Plugin | Angle |
|---|---|
| [octo.nvim](../neovim/octo-nvim.md) | Current. Kitchen sink: issues, PRs, discussions, actions |
| gh-review.nvim | Review only: side-by-side diffs, threads, suggestions, submit. Designed to sit next to gh dash, listing is a non-goal. Most direct "keep dash, better reviewer than octo" swap |
| ghlite.nvim | Lighter octo-ish review, can review without checkout |
| github-pr-reviewer.nvim | Review in real buffers so LSP and `gd` keep working. Covers the Explore gap |
| gh.nvim | Older full review UI built on litee.nvim |
| snacks.nvim | Picker for open PRs and issues, not a review UI. Triage only |
| diffview.nvim + gitsigns | Not GitHub-aware. Checkout or worktree, set gitsigns base to the target branch, review as normal code, comment with something else |

## Candidate flows

Combos to trial, each a full pass through the phases.

| Flow | Triage | Fetch | Diff + Review | Explore | When it fits |
|---|---|---|---|---|---|
| A. Current | gh dash | `gh pr checkout` | octo.nvim | Neovim on branch | Baseline |
| B. Keep dash, swap reviewer | gh dash | none, or checkout | gh dash custom action opens `gh prism <n>` or `:GHReview` (gh-review.nvim) | Neovim on branch if checked out | Dash is fine, octo is the pain point |
| C. Stay in Neovim | snacks / telescope / `:Octo pr list` | `:Octo pr checkout` | gh-review.nvim or ghlite | Same Neovim session | Two tools is one too many |
| D. Deep review in a worktree | gh dash | lazygit worktree, or `git worktree add` | diffview + gitsigns `change_base`, comment with octo / gh-review / prr | Full LSP on the worktree, lazygit for history and rebase, can edit the branch | Big PRs, or when I will push fixes myself |
| E. AI first pass | | | Copilot code review, CodeRabbit, Graphite as a first set of comments | | Layer on top of any of the above, not a replacement |

## Open questions

- Does gh dash or octo.nvim own triage? Having both is one step too many. Flow B keeps dash,
  Flow C drops it.
- Worktree per PR vs checkout in place. Worktrees keep my main working tree clean but need
  a new herdr pane each time. Flow D.
- What tells me a PR I reviewed got a new push, without opening a browser? prtop and
  gh-notify are the candidates.
- Review TUIs (gh-prism, tuicr) skip Fetch entirely. Is losing Explore (no LSP, no `gd`)
  acceptable for small PRs?

## References

- Grok: [Neovim GitHub PR Review Tools](https://grok.com/share/bGVnYWN5_3318b0bb-e326-43a0-840c-438449823b10) -
  source of the dashboard, review TUI, Neovim plugin and candidate flow lists above (2026-10-01)
- Grok: [Neovim Git blame plugins](https://grok.com/share/bGVnYWN5_b3bdb707-58af-4ecb-a69f-4fd22e44d4f3) -
  feeds [neovim-GitLense-options.md](../neovim/neovim-GitLense-options.md)
