### How do I add the pi integration?
`npm install -g @mariozechner/pi-coding-agent`

Then run `pi` once so it creates `~/.pi/agent/`, and quit. After that, run:
`pi v0.73.1`
Warning: No models available. Use /login to log into a provider via OAuth or API key. See:
   /usr/local/lib/node_modules/@mariozechner/pi-coding-agent/docs/providers.md
   /usr/local/lib/node_modules/@mariozechner/pi-coding-agent/docs/models.md

Update Available
New version 1.3.0 is available. Run pi update
Changelog: https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/CHANGELOG.md
 
`sudo npm --prefix /usr/local uninstall -g @mariozechner/pi-coding-agent`
`sudo npm --prefix /usr/local install -g @earendil-works/pi-coding-agent`
`pi`
[1.3.0] - 2026-10-15

`herdr integration install pi`

This writes the extension to `~/.pi/agent/extensions/herdr-agent-state.ts`. 
Restart any running pi sessions afterward so they load it.

### How do I update the claude integration?
herdr integration status shows both as outdated. Claude is v10 and the current version is v11. Grok is v2 and the current version is v3. Re-running install should update them in place:
`herdr integration install claude`
The claude install touches `~/.claude/hooks/herdr-agent-state.sh`. It may also edit your `~/.claude/settings.json` hooks. 
`herdr integration install grok`
The grok install touches `.grok/hooks/herdr-agent-state.sh`.

Restart running Claude and Grok sessions afterward.

   To check the result, run herdr integration status --outdated-only.
