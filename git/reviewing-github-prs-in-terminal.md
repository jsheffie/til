# Reviewing GitHub PRs in the terminal (Neovim + CLI)

Options for reviewing GitHub pull requests without leaving the terminal.

## Neovim plugins

### octo.nvim - `pwntester/octo.nvim`

The most complete in-editor GitHub review tool.

- List, search and open PRs, issues and discussions inside Neovim
- Real review mode (`:Octo review`): side-by-side diff per file, inline comments on lines or ranges, suggested changes, submit as approve / comment / request changes
- Resolve threads, reply to comments, add reactions, change labels and reviewers
- Uses `gh` under the hood, so auth comes from `gh auth login`
- Works with Telescope, fzf-lua or snacks pickers

### diffview.nvim - `sindrets/diffview.nvim`

The best diff viewer in Neovim. Does not talk to GitHub.

```sh
gh pr checkout 123
```

```vim
:DiffviewOpen origin/main...HEAD   " whole PR as a file tree + per-file diff
:DiffviewFileHistory %             " history of the current file
```

Often paired with octo.nvim: diffview for reading the code, octo for commenting.

### gh.nvim - `ldelossa/gh.nvim`

Another full PR review UI, built on litee.nvim. Works, but less active than octo.

### neogit + diffview

Magit-style git UI that uses diffview for diffs. Good for the local git side, no GitHub review features.

## CLI / TUI programs

### gh-dash

```sh
gh extension install dlvhdr/gh-dash
```

The closest thing to "multiplexing" PRs.

- TUI dashboard with configurable sections (e.g. "review requested", "my PRs", "team repo X")
- Keybindings to check out, diff, comment, approve, merge, or open in the browser
- Custom command bindings, e.g. "check out into a worktree and open nvim with octo"
- Diffs go through your pager, so pair it with `delta` or `difftastic`

### prr - `danobi/prr`

Mailing-list style review. Pulls the PR diff into a text file, you type comments inline in Neovim, then `prr submit` posts them as a review. Simple and very editor-native.

### Plain gh

```sh
gh pr list
gh pr checkout 123
gh pr diff 123 | delta
gh pr review 123 --approve
gh pr review 123 --comment -b "looks good"
```

### lazygit / gitui / tig

Great for browsing commits and diffs locally after a checkout. No GitHub review comments.

### Diff pagers

- **delta** - side-by-side diffs with syntax highlighting
- **difftastic** - structural diffs that understand the syntax, great for noisy refactors

## Suggested setup

1. **gh-dash** as the inbox for which PRs need your review
2. A custom gh-dash keybinding that checks the PR out into its own **git worktree** and opens it in a new tmux window, so several reviews stay open side by side and your current branch is never touched
3. In Neovim, **octo.nvim** for the review itself (inline comments, submitting), with **diffview.nvim** for reading large diffs
4. **delta** as the git pager for everything else

Lighter alternative: start with just **prr** or just **octo.nvim**.
