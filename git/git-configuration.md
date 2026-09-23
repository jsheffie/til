I use these aliases daily

- `git lg`
and 
- `git llg`

Imagine my suprise when my new fancy machine did not have them.

added the following alias to my `~/.gitconfig` file

```
[alias]
        st = status
        lg = log --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr %an)%Creset' --abbrev-commit --date=relative -15
        llg = log --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr %an)%Creset' --abbrev-commit --date=relative -245
```