How to contribute to a github open source repo.

**Overview**

1. Fork the Repository
2. Clone the Forked Repository Locally
3. Create a Branch
4. Make Your Changes
5. Push Your Branch to GitHub
6. Create a Pull Request

**Details**

### 1. Fork the Repository

Go to the ffmpeg repository on GitHub: https://github.com/jrottenberg/ffmpeg
Click on the "Fork" button in the top right corner. This creates a copy of the repository under your own account (jsheffie).

### 2. Clone the Forked Repository Locally

You'll need Git installed on your system.
Open a terminal window and use the git clone command to clone your forked repository to your local machine.
The command will look something like:
git clone https://github.com/jsheffie/ffmpeg.git
```
$ gh repo clone jsheffie/ffmpeg-fork
```

### 3. Create a Branch

```
$ cd ffmpeg-fork
$ git checkout -b jds-fix-drawtext-filter-problem
```

### 4. Make Your Changes
- Now you can make your changes to the code in your local repository.
- Edit the relevant files, add them to your staging area with git add, and commit your changes with a descriptive commit message using git commit.

### 5. Push Your Branch to GitHub
Once your changes are committed, push your new branch to your forked repository on GitHub with:
```
git push origin fix-audio-bug  # replace 'fix-audio-bug' with your branch name
```
### 6. Create a Pull Request

- Go to your forked ffmpeg repository on GitHub.
- Click on the "Branch" dropdown menu and select your new branch (e.g., fix-audio-bug).
- Click the green "Pull request" button.
- Fill out the pull request form with a clear description of your changes and why they are beneficial.
- Click "Create pull request" to submit your contribution for review by the ffmpeg maintainers.