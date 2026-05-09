1. GitLens (free, the standard)
Shows inline blame annotations, file/line history, and side-by-side diffs against any branch, commit, or remote. Works in Cursor since it's a VS Code extension. Install from the Extensions panel (Cmd+Shift+X) → search "GitLens" → Install.
For your specific use case (diff against GitHub repo): right-click a file → "Open Changes with..." → pick the branch or commit. You can also use the GitLens sidebar to browse commits and diff against origin/main or any remote ref.

2. GitHub Pull Requests and Issues (Microsoft, free)
Official Microsoft extension. Lets you review PRs directly in Cursor with inline diffs, leave review comments, check out PR branches, and create new PRs. Best if your workflow involves reviewing teammates' PRs without leaving the editor.

3. Git Graph (free)
Visualizes your branch/commit graph and lets you click any commit to see its diff. 
Great if you think visually about git history. Pairs well with GitLens.

4. Built-in Source Control panel
Cursor (via VS Code) already shows uncommitted diffs out of the box 
— just click the Source Control icon in the activity bar (Ctrl+Shift+G). 
Click any changed file and you get a side-by-side diff. No extension needed for the basics.

