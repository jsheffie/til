# Neovim Keybindings & Commands

Quick reference for common Neovim operations.

## Yanking (Copying) Lines

### Visual Mode (Linewise)
- `V` - Enter linewise visual mode
- `j` / `k` - Move selection down/up
- `y` - Yank (copy) selected lines
- `"+y` - Yank selected lines to OS clipboard

### Count Prefix (Quickest)
- `yy` - Yank current line
- `3yy` - Yank 3 lines (replace 3 with desired count)
- `"+yy` - Yank current line to OS clipboard
- `"+5yy` - Yank 5 lines to OS clipboard

### Motion-Based
- `y5j` - Yank from current line down 5 lines
- `y}` - Yank to end of paragraph
- `yG` - Yank to end of file
- `"+y5j` - Yank down 5 lines to OS clipboard

## Pasting

- `p` - Paste after cursor
- `P` - Paste before cursor
- `"+p` - Paste from OS clipboard after cursor
- `"+P` - Paste from OS clipboard before cursor

## OS Clipboard Integration

### Registers
- `+` - OS clipboard (primary on most systems)
- `*` - Primary selection buffer (alternative on some systems)

### Check Clipboard Support
```vim
:echo has('clipboard')
```
Returns `1` if enabled, `0` if disabled.

### Copy to Clipboard Examples
- `"+yy` - Copy current line to OS clipboard
- `"+3yy` - Copy 3 lines to OS clipboard
- `V` → select → `"+y` - Visual selection to OS clipboard

### Paste from Clipboard
- `"+p` - Paste from OS clipboard
- `"+P` - Paste from OS clipboard before cursor

**Note:** When running Neovim in herdr (terminal multiplexer), ensure clipboard access is enabled in your herdr configuration.

## Common Navigation

- `h` `j` `k` `l` - Move left, down, up, right
- `w` - Jump to next word
- `b` - Jump to previous word
- `gg` - Go to beginning of file
- `G` - Go to end of file
- `:<line_number>` - Go to specific line (e.g., `:42`)

## Editing

- `i` - Insert before cursor
- `a` - Insert after cursor
- `o` - Open new line below
- `O` - Open new line above
- `dd` - Delete line
- `d3j` - Delete down 3 lines
- `u` - Undo
- `Ctrl+r` - Redo

## Selection

- `v` - Character-wise visual mode
- `V` - Linewise visual mode
- `Ctrl+v` - Block visual mode

## Search & Replace

- `/pattern` - Search forward
- `?pattern` - Search backward
- `n` - Next match
- `N` - Previous match
- `*` - Search forward for the word under cursor
- `#` - Search backward for the word under cursor
- `:noh` - Clear search highlighting
- `:%s/old/new/g` - Replace all occurrences
- `:%s/old/new/gc` - Replace with confirmation

### Telescope Search

Leader is `Space` (kickstart.nvim config, see `~/.config/nvim/init.lua`).

| Keys | What it does |
|---|---|
| `Space /` | Fuzzy search in the current buffer |
| `Space s g` | Live grep: search contents of all files as you type |
| `Space s w` | Grep the word under cursor (or visual selection) |
| `Space s /` | Live grep limited to open files |
| `Space s r` | Resume the last Telescope search |
| `Space s f` | Search file names (not contents) |
| `Space s k` | Search keymaps |

Inside the Telescope picker:
- `Ctrl-n` / `Ctrl-p` - Move down/up the results
- `Enter` - Open the selected result
- `Ctrl-q` - Send all results to the quickfix list
- `Esc` - Close

Working the quickfix list:
- `:cnext` / `:cprev` - Step through matches
- `:cdo s/old/new/g` - Replace across every match

Live grep and grep word require `ripgrep` (`brew install ripgrep`). Check with `:checkhealth telescope`.

## File Operations

- `:w` - Save
- `:q` - Quit
- `:wq` - Save and quit
- `:q!` - Quit without saving
- `:e <filename>` - Open file
