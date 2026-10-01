# octo.nvim: GitHub Issues & PR Reviews in Neovim

[pwntester/octo.nvim](https://github.com/pwntester/octo.nvim) lets you list, open, edit and
review GitHub issues and pull requests as regular Neovim buffers. Edit a title, body or comment
and `:w` syncs it to GitHub.

## Setup (what I have)

Installed via `vim.pack` in `~/.config/nvim/init.lua`:

```lua
vim.pack.add { gh 'pwntester/octo.nvim' }
require('octo').setup {
  picker = 'telescope',
  file_panel = { icons = vim.g.have_nerd_font },
}
```

- Auth comes from the `gh` CLI (`gh auth login`). Check with `:checkhealth octo`.
- Uses telescope + plenary (already in kickstart) for pickers.
- `render-markdown.nvim` is configured with `file_types = { 'markdown', 'octo' }` so PR/issue
  buffers render as markdown.
- My `<leader>` and `<localleader>` are both `Space`, so `<localleader>ca` = `Space c a`.

## Using it

Restart Neovim, `cd` into a GitHub repo, then:

| Command | What it does |
|---|---|
| `:Octo pr list` | Browse and open PRs (telescope picker, `Enter` to open) |
| `:Octo issue list` | Browse issues |
| `:Octo review start` | Start reviewing the PR you have open |
| `:Octo review submit` | Submit the review |
| `:Octo pr browser` | Open the current PR in the browser |

From any octo buffer, press `Enter` in normal mode to see common actions.

## Open a specific PR

Any of these work:

```vim
:Octo pr edit 123                                  " PR #123 in the current repo
:Octo pr edit 123 owner/repo                       " PR #123 in another repo
:Octo https://github.com/owner/repo/pull/123       " paste a GitHub URL
:e octo://owner/repo/pull/123                      " works from any directory
:Octo pr changes                                   " file changes, works with teloscope
:Octo pr commits                                   " pr commits
```

`:Octo pr checkout` (inside the PR buffer) checks the PR branch out locally.

## Review a PR and comment on the code diff

1. Open the PR (see above), then `:Octo review start`
   (`:Octo review resume` continues a pending review).
2. A new tab opens: changed-files panel on the left, two-way diff on the right.
   - `]q` / `[q` next / previous changed file
   - `]t` / `[t` next / previous comment thread
   - `Space e` focus the file panel, `Space b` hide/show it
3. Put the cursor on a line in the **right** (new code) or **left** (old code) diff window.
   - Single line: `Space c a`
   - Multiple lines: select with `V` + `j`/`k`, then `Space c a`
   - Suggested change instead of a comment: `Space s a`
4. A comment buffer opens in the other diff window. Type the comment and `:w` to save it to
   the pending review.
5. `:Octo review submit` (or `Space v s`) opens a float for the top-level summary. Leave insert
   mode, then:
   - `Ctrl-m` comment only
   - `Ctrl-a` approve
   - `Ctrl-r` request changes

`:Octo review comments` lists your pending comments (`Enter` jumps to one).
`:Octo review discard` throws the pending review away.

## Commenting on lines away from the diff

**Short version: octo.nvim can only comment on lines inside a diff hunk.** A hunk is the
changed lines plus ~3 unchanged context lines around them. Commentable lines are marked in
the sign column of the review diff. Anything else gives:

```
Cannot place comments outside diff hunks
```

This is a GitHub API limitation, not just octo: the review-comment API rejects lines outside
the diff hunks (`"pull_request_review_thread.line" is not part of the diff`). A multi-line
selection also has to fit inside a single hunk.

GitHub's **web UI** (new "Files changed" page, since Sept 2025) and **GitHub Mobile**
(since Feb 2026) *can* comment on unchanged lines. Their API does not yet.

Ways to handle it:

1. **Anchor on the nearest commentable line and link to the far lines** (stays in Neovim).
   In the review diff, `Ctrl-e` copies the commit SHA. Build a permalink and paste it in the
   comment:
   ```
   See also https://github.com/owner/repo/blob/<sha>/path/to/file.py#L120-L130
   ```
   GitHub renders that permalink as an inline code snippet in the comment.
2. **Use the web UI for that one comment.** `:Octo pr browser`, go to **Files changed**,
   expand the context above/below the hunk, and click `+` on the unchanged line. It lands in
   the same PR review conversation.
3. **General PR comment.** In the PR buffer, `:Octo comment add` for a non-line comment, or put
   it in the top-level summary when you `:Octo review submit`.

## Videos

| Video | Channel | Notes |
|---|---|---|
| [Reviewing GitHub Pull Requests in your Terminal](https://www.youtube.com/watch?v=0VbWVNWeo7M) | Zachary Proser | gh-dash + octo.nvim full review workflow ([write-up](https://zackproser.com/videos/video-reviewing-github-prs-in-terminal)) |
| [Use Github in Neovim - octo.nvim](https://www.youtube.com/watch?v=ERC2mn5jKnA) | Andrew Courter | Viewing/editing PRs, issues and reviews |
| [GitHub INSIDE Neovim?! Code Reviews, PR Comments & More](https://www.youtube.com/watch?v=hd_rnOA1Q5U) | Sam Natale | Code reviews and PR comments in octo |
| [How to Review a PR without Leaving the Terminal (Neovim)](https://www.youtube.com/watch?v=VFESU67M4bk) | Simon Späti | Uses the alternative `ldelossa/gh.nvim` plugin; good for comparison |

## References

- octo.nvim README (commands + default keymaps): https://github.com/pwntester/octo.nvim
- `:help octo`
- Commenting on unchanged lines (web UI): https://github.blog/changelog/2025-09-25-pull-request-files-changed-public-preview-now-supports-commenting-on-unchanged-lines/
- Commenting on unchanged lines (mobile): https://github.blog/changelog/2026-02-03-github-mobile-comment-on-unchanged-lines-in-pull-request-files/
- API request to allow comments anywhere in changed files: https://github.com/orgs/community/discussions/187218
