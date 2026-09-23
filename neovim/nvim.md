# Neovim: Install & Basic Usage

Neovim (`nvim`) is a fork of Vim that modernizes the internals (async job control, a real
plugin API, embedded Lua) while staying command-compatible with Vim. If you already know
vi/vim, your muscle memory transfers directly.

## Install

### macOS (Homebrew)

```
brew install neovim
```

Brew suggested these deps and I said yes:
``
lpeg
luajit
luv
tree-sitter
unibilium
```

### Linux

```
# Debian/Ubuntu (apt often ships an old version — check with `nvim --version`)
sudo apt install neovim

# Fedora
sudo dnf install neovim

# Arch
sudo pacman -S neovim
```

If your distro's package is stale, grab the latest AppImage or tarball from the
[Neovim releases page](https://github.com/neovim/neovim/releases).

### Windows

```
winget install Neovim.Neovim
# or
choco install neovim
```

### Verify

```
nvim --version
```

## Basic Usage

Neovim keeps Vim's modal editing model:

- **Normal mode** — the default; keys are commands, not text input.
- **Insert mode** — press `i` to enter, type text, `Esc` to leave.
- **Visual mode** — press `v` to select text, `Esc` to leave.
- **Command-line mode** — press `:` to run commands (save, quit, search/replace, etc.).

### Opening and closing

```
nvim file.txt     # open a file
nvim .             # open the built-in file explorer in the current directory
```

| Command | Effect |
|---|---|
| `:w` | save |
| `:q` | quit |
| `:wq` or `ZZ` | save and quit |
| `:q!` | quit without saving |

### Moving around (Normal mode)

| Key | Effect |
|---|---|
| `h` `j` `k` `l` | left / down / up / right |
| `w` / `b` | next / previous word |
| `0` / `$` | start / end of line |
| `gg` / `G` | start / end of file |
| `:n` | go to line `n` |

### Editing (Normal mode)

| Key | Effect |
|---|---|
| `i` / `a` | insert before / after cursor |
| `o` / `O` | open new line below / above |
| `x` | delete character under cursor |
| `dd` | delete (cut) current line |
| `yy` | yank (copy) current line |
| `p` / `P` | paste after / before cursor |
| `u` | undo |
| `Ctrl-r` | redo |
| `/pattern` | search forward |
| `:%s/old/new/g` | replace all occurrences on all lines |

### Getting help

```
:help             " open help
:help <topic>     " help for a specific command, e.g. :help dd
:checkhealth      " diagnose your Neovim setup
```

### Config file location

Vim reads `~/.vimrc`. Neovim reads Lua (or Vimscript) from:

```
~/.config/nvim/init.lua     # preferred
~/.config/nvim/init.vim     # also supported
```

A minimal starting config:

```lua
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.expandtab = true
vim.opt.shiftwidth = 2
vim.opt.tabstop = 2
vim.opt.ignorecase = true
vim.opt.smartcase = true
```

## vi/vim vs Neovim — Key Differences

| Area | vi / Vim | Neovim |
|---|---|---|
| **Config language** | Vimscript (`.vimrc`) | Lua (`init.lua`), Vimscript still works |
| **LSP (autocomplete, go-to-def, diagnostics)** | Not built in; needs plugins (coc.nvim, YouCompleteMe) | Built-in LSP client (`vim.lsp`); pair with a server via `nvim-lspconfig` |
| **Syntax highlighting** | Regex-based | Regex-based, with an optional built-in Tree-sitter parser for accurate, AST-based highlighting |
| **Async / job control** | Vim 8+ has jobs, but limited API | First-class async API (`vim.loop`/libuv), plugins don't block the UI |
| **Embedded scripting** | Vimscript only (Vim 9 adds Vim9script) | Vimscript **and** Lua, with a documented Lua stdlib (`vim.*`) |
| **Plugin ecosystem** | Mature, huge (Vim 8 native package support) | Same ecosystem mostly works, plus Lua-native plugins (lazy.nvim, telescope.nvim, etc.) |
| **Terminal emulator** | None built in | `:terminal` opens a real terminal buffer |
| **Remote/plugin API** | Limited (`--servername` on some builds) | RPC API (msgpack) — the basis for GUIs, IDE integrations (VSCode-Neovim, etc.) |
| **Defaults** | Very minimal, `vi`-compatible by default | Saner out-of-the-box defaults (syntax on, incremental search, etc.) even before any config |
| **Distribution** | `vi` ships on virtually every Unix system | Not preinstalled anywhere; you always install it explicitly |

**Bottom line:** if you already know vi/vim commands, they work unchanged in Neovim. The
practical reasons to prefer Neovim are built-in LSP support, Tree-sitter highlighting, a
real async plugin API, and Lua configuration — all things that historically required
bolting plugins onto Vim.

## Further Reading

- [neovim.io](https://neovim.io/)
- [Neovim GitHub](https://github.com/neovim/neovim)
- `:help nvim-from-vim` inside Neovim itself
