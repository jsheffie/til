```
$ git remote add upstream https://github.com/jrottenberg/ffmpeg.git

$ git remote -v
origin	https://github.com/jsheffie/ffmpeg.git (fetch)
origin	https://github.com/jsheffie/ffmpeg.git (push)
upstream	https://github.com/jrottenberg/ffmpeg.git (fetch)
upstream	https://github.com/jrottenberg/ffmpeg.git (push)

$ git fetch upstream
$ git status
On branch jds-Ubuntu-template-22.04-Jammy-Jellyfish
Your branch is up to date with 'origin/jds-Ubuntu-template-22.04-Jammy-Jellyfish'.

$ git merge jrottenberg/ffmpeg:jds-Ubuntu-template-22.04-Jammy-Jellyfish
```