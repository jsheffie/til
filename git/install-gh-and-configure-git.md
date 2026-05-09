
```sh
which gh
```

If not installed, install it.
Can use brew or script ( I used brew on my personal laptop )

```sh
brew install gh
```
or 

```sh
curl -sS https://webi.sh/gh | sh
```

Now the things:
```sh
gh auth login
gh api user -q ".login"
GITHUB_USERNAME=$(gh api user -q ".login")
git config --global user.name "${GITHUB_USERNAME}"
git config --global user.email "${USER_EMAIL}"
echo ${GITHUB_USERNAME}
echo ${USER_EMAIL}
```