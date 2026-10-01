
[Effective Neovim: Instant IDE](https://www.youtube.com/watch?v=stqUbv-5u2s)

- vimtutor  ( is a command line app )
- [ThePrimogen Vim as your editor](https://www.youtube.com/watch?v=X6AR2RMB5tE&list=PLm323Lc7iSW_wuxqmKx_xxNtJC_hJbQ7R)

One simple script for to get the initial install
- IDE -> PDE ( Personalised Development Environment )

1. mkdir -p .config/nvim

2. [kickstart nvim](https://github.com/nvim-lua/kickstart.nvim)

3. Install prereqs: (what I was missing) `brew install tree-sitter-cli fd`

4. Copy the `init.lua` from the repo to `~/.config/nvim`

5. Launch `nvim` it reads the `init.lua` and does the things

`shift <` - opens navigate window

`space sf`  - search files 





## Enabled plugins

Managed with Neovim's built-in `vim.pack` (see `~/.config/nvim/init.lua`, lockfile in `nvim-pack-lock.json`).

### Colorschemes

- [tokyonight.nvim](https://github.com/folke/tokyonight.nvim)
- [rose-pine/neovim](https://github.com/rose-pine/neovim)
- [kanagawa.nvim](https://github.com/rebelot/kanagawa.nvim)
- [catppuccin/nvim](https://github.com/catppuccin/nvim) - active colorscheme

### Editing and UI

- [guess-indent.nvim](https://github.com/NMAC427/guess-indent.nvim) - detect tabstop and shiftwidth automatically
- [gitsigns.nvim](https://github.com/lewis6991/gitsigns.nvim) - git signs in the gutter and hunk navigation
- [which-key.nvim](https://github.com/folke/which-key.nvim) - show pending keybinds
- [todo-comments.nvim](https://github.com/folke/todo-comments.nvim) - highlight TODO, NOTE, etc in comments
- [mini.nvim](https://github.com/nvim-mini/mini.nvim) - modules enabled: `mini.icons`, `mini.ai`, `mini.surround`
- [fidget.nvim](https://github.com/j-hui/fidget.nvim) - LSP progress notifications
- [render-markdown.nvim](https://github.com/MeanderingProgrammer/render-markdown.nvim) - render markdown in the buffer (`space tm` to toggle)

### Fuzzy finding

- [plenary.nvim](https://github.com/nvim-lua/plenary.nvim) - lua utility library used by telescope and octo
- [telescope.nvim](https://github.com/nvim-telescope/telescope.nvim) - fuzzy finder
- [telescope-ui-select.nvim](https://github.com/nvim-telescope/telescope-ui-select.nvim) - use telescope for `vim.ui.select`
- [telescope-fzf-native.nvim](https://github.com/nvim-telescope/telescope-fzf-native.nvim) - fzf sorter (only installed when `make` is available)

### LSP, completion, formatting

- [nvim-lspconfig](https://github.com/neovim/nvim-lspconfig) - LSP server configs
- [mason.nvim](https://github.com/mason-org/mason.nvim) - install LSP servers, formatters, linters
- [mason-lspconfig.nvim](https://github.com/mason-org/mason-lspconfig.nvim) - bridge mason and lspconfig
- [mason-tool-installer.nvim](https://github.com/WhoIsSethDaniel/mason-tool-installer.nvim) - auto-install tools listed in `init.lua`
- [conform.nvim](https://github.com/stevearc/conform.nvim) - formatting
- [LuaSnip](https://github.com/L3MON4D3/LuaSnip) - snippet engine
- [blink.cmp](https://github.com/saghen/blink.cmp) - autocompletion
- [nvim-treesitter](https://github.com/nvim-treesitter/nvim-treesitter) - syntax highlighting and parsers (`main` branch)

### GitHub

- [octo.nvim](https://github.com/pwntester/octo.nvim) - GitHub issues and PR reviews, see notes below

## Plugin notes

- [octo.nvim: GitHub issues & PR reviews](octo-nvim.md)
