# Neovim options for GitLens (GitKraken) features

[GitLens](https://gitlens.amod.io/) is a VS Code extension by GitKraken. No single Neovim plugin
replaces all of it, but a small set of plugins covers the parts that matter. This is a list of
things to explore, grouped by the GitLens feature they replace.

## Already installed

[gitsigns.nvim](https://github.com/lewis6991/gitsigns.nvim) is already in my `init.lua` (gutter
signs and hunk navigation). It also does most of the GitLens blame features, so start there before
adding anything.

## GitLens feature map

| GitLens feature | Neovim answer | Status |
|---|---|---|
| Current line blame (author, date, message at end of line) | gitsigns `current_line_blame` | Installed, not enabled |
| Hover with full commit details | gitsigns `blame_line` | Installed |
| File blame annotations (whole file) | gitsigns `:Gitsigns blame` | Installed |
| Hunk preview, stage, reset | gitsigns | Installed |
| File history / line history | diffview.nvim, telescope git pickers | To explore |
| Commit graph, branches, stashes UI | neogit, lazygit | To explore |
| Compare branches or commits | diffview.nvim | To explore |
| Open file or line on GitHub | gitlinker.nvim, snacks.nvim `gitbrowse` | To explore |
| PRs and issues | octo.nvim | Installed, see [octo-nvim.md](octo-nvim.md) |
| Merge conflict helpers | git-conflict.nvim | To explore |

## 1. Inline blame (the headline GitLens feature)

### Option A: gitsigns (recommended first step)

No new plugin. Turn it on in the existing gitsigns `setup()`:

```lua
require('gitsigns').setup {
  current_line_blame = true,
  current_line_blame_opts = {
    virt_text = true,
    virt_text_pos = 'eol', -- 'eol' | 'overlay' | 'right_align'
    delay = 400,           -- default is 1000ms, GitLens feels more instant
  },
  current_line_blame_formatter = '<author>, <author_time:%R> - <summary>',
}
```

Useful commands:

- `:Gitsigns toggle_current_line_blame` - turn inline blame on or off
- `:Gitsigns blame_line` - popup with the commit for the current line
- `:Gitsigns blame` - blame the whole file in a side window

### Option B: dedicated blame plugins

Only worth it if gitsigns blame is not enough.

- [f-person/git-blame.nvim](https://github.com/f-person/git-blame.nvim) - the most common
  blame-only plugin. Virtual text plus `:GitBlameToggle`. Can open the commit on the web
  (`:GitBlameOpenCommitURL`).
- [FabijanZulj/blame.nvim](https://github.com/FabijanZulj/blame.nvim) - fugitive-style side-by-side
  blame view with commit colouring. Closer to GitLens "file annotations".
- [APZelos/blamer.nvim](https://github.com/APZelos/blamer.nvim) - describes itself as inspired by
  GitLens. Vimscript, older.

## 2. File history and compare

- [sindrets/diffview.nvim](https://github.com/sindrets/diffview.nvim) - the closest thing to
  GitLens history and compare views.
  - `:DiffviewFileHistory %` - history of the current file
  - `:DiffviewFileHistory` with a visual selection - history of a line range
  - `:DiffviewOpen main...HEAD` - compare my branch to main
  - `:DiffviewClose`
- Telescope git pickers (telescope is already installed, no new plugin):
  - `:Telescope git_commits` - repo commits
  - `:Telescope git_bcommits` - commits touching the current buffer
  - `:Telescope git_branches`, `:Telescope git_stash`
- [aaronhallaert/advanced-git-search.nvim](https://github.com/aaronhallaert/advanced-git-search.nvim) -
  telescope extension for searching commits, diffs and file history. Depends on fugitive and
  diffview.

## 3. Full git UI (graph, branches, stash, rebase)

GitLens has a "Commit Graph" and side bar views. In Neovim pick one of these:

- [NeogitOrg/neogit](https://github.com/NeogitOrg/neogit) - Magit-style git interface inside
  Neovim. Integrates with diffview and telescope.
- [kdheepak/lazygit.nvim](https://github.com/kdheepak/lazygit.nvim) - opens the `lazygit` TUI in a
  floating window. Needs `brew install lazygit`. Best graph and interactive rebase experience with
  the least config.
- [tpope/vim-fugitive](https://github.com/tpope/vim-fugitive) - the classic. `:Git`, `:Git blame`,
  `:Gdiffsplit`. Not inline, but a very complete command set.

## 4. Open on GitHub and share links

GitLens has "Open on Remote" and "Copy Remote URL".

- [ruifm/gitlinker.nvim](https://github.com/ruifm/gitlinker.nvim) - copy a permalink to the
  current line or visual selection.
- [folke/snacks.nvim](https://github.com/folke/snacks.nvim) - has a `gitbrowse` module (open or
  copy the GitHub URL) and a `lazygit` module. Also a large collection of other utilities, so
  review before adopting.
- [tpope/vim-rhubarb](https://github.com/tpope/vim-rhubarb) - GitHub support for fugitive
  (`:GBrowse`).

## 5. Merge conflicts

- [akinsho/git-conflict.nvim](https://github.com/akinsho/git-conflict.nvim) - highlights conflict
  markers and gives choose-ours, choose-theirs, choose-both and next/previous mappings.

## What does not have a Neovim equivalent

- GitLens Visual File History (the interactive timeline graphic)
- "Worktrees" and "Launchpad" sidebar views
- AI commit message and explain-commit features (look at a general Neovim AI plugin instead)

## Suggested order to explore

1. Enable `current_line_blame` in the existing gitsigns config (no new plugin).
2. Add `diffview.nvim` for file history and branch compare.
3. Try `lazygit.nvim` or `neogit` for the graph and branch UI. Pick one, not both.
4. Add `gitlinker.nvim` for permalinks if I share code links often.
5. Only add a dedicated blame plugin if gitsigns blame feels lacking.

## Notes

- Plugin names and commands above are from memory and a Grok conversation on this topic, not
  checked against each plugin's current docs. Read the README before installing.
- My plugins are managed with `vim.pack` (see [README.md](README.md)), so add each one with
  `vim.pack.add { gh 'owner/repo' }` like octo.nvim.
