# Neovim code folding

## Basic fold commands (normal mode)

| Key | Action |
|-----|--------|
| `zc` | Close fold under cursor |
| `zo` | Open fold under cursor |
| `za` | Toggle fold under cursor |
| `zC` / `zO` / `zA` | Same, but recursive (nested folds) |
| `zM` | Close all folds in the buffer |
| `zR` | Open all folds in the buffer |
| `zm` / `zr` | Fold one level more / less |
| `zj` / `zk` | Move to next / previous fold |
| `zd` | Delete the fold under cursor (manual/marker methods) |
| `zE` | Eliminate all folds (manual method) |
| `zf{motion}` | Create a fold (manual method), e.g. `zfap` folds a paragraph |
| `:{range}fold` | Create a fold for a line range |

## Choosing a fold method

Set `foldmethod` to control how folds are computed:

```lua
vim.opt.foldmethod = "indent"   -- based on indentation
vim.opt.foldmethod = "syntax"   -- based on the syntax file
vim.opt.foldmethod = "marker"   -- based on {{{ }}} markers
vim.opt.foldmethod = "manual"   -- you create them with zf (default)
vim.opt.foldmethod = "expr"     -- based on foldexpr
```

## Treesitter-based folding (recommended)

For most languages, treesitter folds are the best option. Neovim has built-in support:

```lua
vim.opt.foldmethod = "expr"
vim.opt.foldexpr = "v:lua.vim.treesitter.foldexpr()"
```

You need the treesitter parser installed for the language (for example via `nvim-treesitter`). On older Neovim versions, use `nvim_treesitter#foldexpr()` instead.

## Useful options

```lua
vim.opt.foldlevelstart = 99   -- open all folds when opening a file
vim.opt.foldlevel = 99        -- keep folds open by default
vim.opt.foldenable = true     -- enable folding
vim.opt.foldcolumn = "1"      -- show a fold indicator column
vim.opt.foldnestmax = 4       -- limit nesting depth (indent/syntax)
```

`foldlevelstart = 99` is worth setting. Without it, files open fully folded with expr/indent methods.

## Plugin option

[nvim-ufo](https://github.com/kevinhwang93/nvim-ufo) gives VS Code-style folding, with better previews and LSP or treesitter fold providers. It needs `foldlevel = 99` and `foldlevelstart = 99`, and it is usually paired with its `zR` / `zM` remaps (`require("ufo").openAllFolds` / `closeAllFolds`).

For help inside Neovim, run `:help folding`.
