How do you tell what is installed in homebrew
Here are the main commands:

```bash
brew list              # everything installed (formulae and casks)
brew list --formula    # only command-line packages (formulae)
brew list --cask       # only GUI apps (casks)
brew leaves            # only top-level packages you installed explicitly (no dependencies)
brew leaves --installed-on-request   # same idea, stricter about what you asked for
```

Other useful ones:

```bash
brew list --versions          # include version numbers
brew info <name>              # details on one package, including whether it's installed
brew deps --installed --tree  # dependency tree of what's installed
brew uses --installed <name>  # which installed packages depend on <name>
brew outdated                 # installed packages with newer versions available
brew autoremove --dry-run     # orphaned dependencies that could be removed
```

`brew leaves` is usually the most useful. It shows what you chose to install, without the long list of dependencies.

To snapshot everything, including taps, into a file, run `brew bundle dump --file=~/Brewfile`. You can reinstall from that file on another machine with `brew bundle --file=~/Brewfile`. That would fit well in this dotfiles repo as a new module.

Homebrew doesn't track apps you installed by dragging them into `/Applications`, so those won't appear.


## How I noticed things installed under the covers
I noticed the other day while updateing `herdr`
that there is a file that represents sym links to everything installed.

`ls -al  /opt/homebrew/share/zsh/site-functions/`


## What I have installed and why:

_bat
_brew
_delta
_fd
_gh
_ghostty
_gitleaks
_glow
_gum
_herdr
_hugo
_just
_mdcat
_p11-kit
_pnpm
_rbenv
_rg
_rustup
_the_silver_searcher
_tree-sitter
_trust
_uv
_uvx
