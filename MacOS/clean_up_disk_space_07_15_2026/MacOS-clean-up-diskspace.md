

1. `brew install ncdu`
2. take snapshot ( before deep clean )


```
ncdu ~          # Start in your home directory
# or
ncdu /         # Whole system (will take a minute, skip protected dirs)
```

```
# Top 10 largest items in current dir
du -sh * | sort -hr | head -n 10

# In your home (or /)
du -sh ~/Library/* | sort -hr | head -n 15

# Large files overall
find ~ -type f -size +500M -exec ls -lh {} \; | sort -k5 -hr
```

```
brew cleanup -s          # Remove old downloads and cache
brew autoremove          # Remove unused dependencies
brew doctor
```

```
~/Library/Caches/ and ~/Library/Application Support/ (especially Docker, Xcode, Steam, browsers, IDEs).
Old Docker images/volumes: docker system prune -a
Node modules, Python venvs, build artifacts.
Time Machine local snapshots (if enabled): tmutil listlocalsnapshots / and tmutil thinlocalsnapshots / 999999999999
```