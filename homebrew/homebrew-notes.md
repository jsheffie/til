# Homebrew Notes

## Cask commands (e.g. spacemap via `jsheffie/tap`)

**1. Check if installed**
```bash
brew list --cask spacemap
```
Or for more detail:
```bash
brew info --cask jsheffie/tap/spacemap
```

**2. Remove it**
```bash
brew uninstall --cask spacemap
```

**3. Refresh / update tap (pick up formula/cask changes)**
```bash
brew update
```
This re-fetches all taps including `jsheffie/tap`. If you want to refresh just that tap:
```bash
brew tap --force jsheffie/tap
```

**4. Install**
```bash
brew install --cask jsheffie/tap/spacemap
```

---

**Typical update workflow** (remove old, pull changes, reinstall):
```bash
brew uninstall --cask spacemap && brew update 
Manually remove the System Settings -> Privacy & Secturity -> Accessibility entry for spacemap (press -)
then:
brew install --cask jsheffie/tap/spacemap
```

```sh
spctl --assess --verbose /Applications/spacemap.app
codesign --verify --deep --verbose /Applications/spacemap.app
```
And also:
```sh
codesign -dv --verbose=4 /Applications/spacemap.app
```

```sh
The signature is valid (flags=0x2(adhoc)) but TeamIdentifier=not set and Signature=adhoc — that's the problem. On modern macOS
  (Ventura+), spctl rejects ad-hoc signed apps from the internet even with no quarantine flag, because there's no team ID to verify
  against.

  Check if the quarantine flag is actually gone:

  ! xattr /Applications/spacemap.app
```

The quarantine flag is still there — disable_quarantine true in the Cask isn't working. That's likely because the Cask is in
  Casks/spacemap.rb but the tap might be serving the Formula version instead.

  Try manually stripping it:

  ! sudo xattr -rd com.apple.quarantine /Applications/spacemap.app

  Then try opening it again. If that works, we know the fix is just getting disable_quarantine true to actually apply during
  install.

ps aux | grep spacemap | grep -v grep

