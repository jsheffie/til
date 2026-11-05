Migrate my terminal setup to Rex, the terminal multiplexer this terminal runs in.
Read nothing beyond this prompt: "Rex in brief" below has what the iTerm2 section
need. The other sections carry their bindings already translated and verified by Rex;
write those lines as given and look nothing up for them.

## Before reading anything, ask me about cmd+k
Rex binds cmd+k to session.switch, the session picker. Terminal.app, iTerm2 and Ghostty
use cmd+k to clear the terminal. Ask me which I want, and wait for my answer:
1. Keep the session picker on cmd+k. Nothing changes.
2. Clear the terminal on cmd+k. Bind cmd+k to the server action
   com.superlogical.terminal.clear ("Clear Terminal"). The session picker then needs
   another key: propose shift+cmd+k, which Rex binds nothing to, let me change it, and
   bind session.switch there.
If cmd+k changes, list it under "Replaced Rex defaults" in the report as "cmd+k: no
longer opens the session picker (Rex default); now clears the terminal, by my decision;
the picker is on <key>".

## Read these files, and nothing else in my home directory

- Herdr:
  - /Users/jds/.config/herdr/config.toml
  Found: prefix ctrl+b, 2 bindings run commands, theme catppuccin.
- Ghostty:
  - /Users/jds/.config/ghostty/config
  - /Users/jds/Library/Application Support/com.mitchellh.ghostty/config.ghostty
  Found: theme Catppuccin Mocha.
- iTerm2:
  - /Users/jds/Library/Preferences/com.googlecode.iterm2.plist
  Note: the settings are a binary property list; read them with "plutil -convert json -o - <path>" or "defaults export com.googlecode.iterm2 -".

## Write here
/Users/jds/.config/rex/init.lua
The file does not exist yet. Create it, and its directory if needed.
Every command below names this file with REX_CONFIG, so nothing in your shell's
environment can point them at another file.


## Rex in brief
- A key is modifiers and one key joined with `+`: `ctrl+a`, `shift+cmd+d`. Rex spells
  modifiers in the order ctrl, alt, shift, cmd; `super` and `command` mean cmd, `opt` and
  `option` mean alt and `control` means ctrl.
- Named keys: enter, esc, tab, space, backspace, delete, insert, home, end, pageup,
  pagedown, left, right, up, down, f1 to f25. Any other key is its own character: `-`,
  `=`, `,`, `[`, `` ` ``.
- Keys are unshifted, as a US key cap reads, and a capital letter is `shift+` the letter:
  `!` is `shift+1`, `"` is `shift+'`, `#` is `shift+3`, `$` is `shift+4`, `%` is
  `shift+5`, `&` is `shift+7`, `(` is `shift+9`, `)` is `shift+0`, `*` is `shift+8`, `+`
  is `shift+=`, `:` is `shift+;`, `<` is `shift+,`, `>` is `shift+.`, `?` is `shift+/`,
  `@` is `shift+2`, `^` is `shift+6`, `_` is `shift+-`, `{` is `shift+[`, `|` is
  `shift+\`, `}` is `shift+]`, `~` is `shift+``.
- A sequence is keys pressed one after another, joined with `>`: `rex.bind("ctrl+a>c",
  "client.tab.new")`. A key that starts a sequence cannot also run an action.
- `rex.bind(key, action[, args])`: `rex.bind("cmd+d", "pane.split", { direction = "right" })`.
  `rex.unbind(key[, action])` removes a key's bindings, Rex's own default included:
  `rex.unbind("cmd+k")`. A later rex.bind of the same key replaces an earlier one.
- For anything no action does: `rex.action{ name = "x", title = "X", args = { what = "string?" },
  run = function(ctx, args) ... end }`, then bind "x". Inside run, `rex.exec{ "cmd", "arg" }`
  runs a command and `rex.client.queue("pane.zoom", {})` performs an app action.

The actions a key can be bound to, with their arguments (`?` marks an optional one). Only an
action marked "also" has dotted names such as `pane.split.right`, which is `pane.split` with
`{ direction = "right" }`; every other action is bound by its name with arguments.
- client.window.new: New Window
- client.window.close: Close Window
- client.window.fullscreen.toggle: Toggle Full Screen
- client.palette.toggle: Command Palette…
- session.new: New Session
- session.switch: Change Session…
- session.next: Next Session
- session.previous: Previous Session
- session.rename: Rename Session
- session.close: Close Session
- session.refresh: Refresh Sessions
- session.collapse { session_id? = string }: Collapse Session
- session.expand { session_id? = string }: Expand Session
- session.collapse_others { session_id? = string }: Collapse Other Sessions
- client.tab.new: New Tab
- client.tab.close: Close Tab
- client.tab.rename: Rename Tab
- client.tab.next: Show Next Tab
- client.tab.previous: Show Previous Tab
- client.tab.goto { index = integer }: Go to Tab
- client.tab.move { direction = backward|forward }: Move Tab (also client.tab.move.backward, .forward)
- client.tab.move_to_new_window: Move Tab to New Window
- pane.split { direction = right|down|left|up|auto }: Split Pane (also pane.split.right, .down, .left, .up, .auto)
- pane.focus { direction = left|right|up|down, wrap? = boolean }: Focus Pane (also pane.focus.left, .right, .up, .down)
- pane.focus_next: Focus Next Pane
- pane.focus_previous: Focus Previous Pane
- pane.move { direction = left|right|up|down }: Move Pane (also pane.move.left, .right, .up, .down)
- pane.float: Float Pane
- pane.minimize_floating: Minimize Floating Window
- pane.minimize_all_floating: Minimize Floating Windows
- pane.zoom: Zoom Pane
- pane.close: Close Pane
- pane.balance: Balance Splits
- pane.resize { amount? = number, direction = left|right|up|down }: Resize Pane (no pane.resize.left: pass direction)
- pane.move_to_new_tab: Move Pane to New Tab
- pane.copy_id: Copy Pane ID
- pane.send_key { key = string }: Send Key
- client.prompt.previous: Jump to Previous Prompt
- client.prompt.next: Jump to Next Prompt
- client.mode.enter { name = string, once? = boolean }: Enter Mode
- client.mode.exit: Exit Mode
- client.mode.exit_all: Exit All Modes
- client.find.open: Find…
- client.find.next: Find Next
- client.find.previous: Find Previous
- client.font.increase: Increase Font Size
- client.font.decrease: Decrease Font Size
- client.font.reset: Reset Font Size
- client.config.reload: Reload Config
- com.superlogical.terminal.clear: Clear Terminal (a server action).
Bind only these names or your own rex.action. For anything else,
`'/Users/jds/Library/Application Support/com.superlogical.rex/RexServer/Versions/1758/Rex Server.app/Contents/MacOS/rex' -S 'unix:///Users/jds/Library/Application%20Support/rex/server.sock' actions --json` lists every action,
and https://www.superlogical.com/rex/docs/llms.txt indexes the documentation, as a last resort.

## Rules for keys
- Keys are written unshifted, as the key cap reads on a US layout: `%` is `shift+5`,
  `"` is `shift+'`, `|` is `shift+\`, `+` is `shift+=`, `_` is `shift+-`, `?` is `shift+/`.
  The unshifted characters stay plain: `-` is `-`, `=` is `=`, `,` is `,`, `\` is `\`.
- `C-a` means `ctrl+a`, `M-x` means `alt+x`, and `super` or `cmd` is `cmd`.
- A capital letter in a source binding is shift and the letter: tmux's `bind H` is
  `shift+h`, and it stays `shift+h` inside a mode, as `resize/shift+h`. Never drop the
  shift to make a key look simpler.
- A key either runs an action or starts a sequence, never both. A sequence such as
  `ctrl+a>c` means ctrl+a alone no longer reaches the terminal. Add
  `rex.bind("ctrl+a>ctrl+a", "pane.send_key", { key = "ctrl+a" })` so programs that use
  the prefix key themselves still receive it, unless a line below already does.
- A binding in init.lua replaces Rex's default on the same key. That is allowed, but a
  line identical to a default is not written, and every default you replace goes in the
  report as "<key>: no longer <what> (Rex default); now <what> from <file:line>". Rex's
  defaults, each as the key and what it does: cmd+n opens a new window; shift+cmd+w closes the window; ctrl+cmd+f toggles full screen; cmd+w closes the pane; shift+cmd+p opens the command palette; cmd+, opens Settings; shift+cmd+, opens Diagnostics; shift+cmd+u installs a waiting update; alt+shift+cmd+u installs a waiting update once Rex is idle; shift+cmd+. dismisses a notice; shift+cmd+n creates a session; cmd+k opens the session picker; cmd+r refreshes the session list; cmd+t opens a new tab; alt+cmd+w closes the tab; ctrl+tab goes to the next tab; shift+cmd+] goes to the next tab; ctrl+shift+tab goes to the previous tab; shift+cmd+[ goes to the previous tab; cmd+[Digit1] goes to tab 1; cmd+[Digit2] goes to tab 2; cmd+[Digit3] goes to tab 3; cmd+[Digit4] goes to tab 4; cmd+[Digit5] goes to tab 5; cmd+[Digit6] goes to tab 6; cmd+[Digit7] goes to tab 7; cmd+[Digit8] goes to tab 8; cmd+[Digit9] goes to the last tab; ctrl+shift+pageup moves the tab left; ctrl+shift+pagedown moves the tab right; cmd+d splits the pane to the right; shift+cmd+right splits the pane to the right; shift+cmd+d splits the pane downward; shift+cmd+down splits the pane downward; shift+cmd+left splits the pane to the left; shift+cmd+up splits the pane upward; cmd+enter splits the pane along its longer side; alt+cmd+left focuses the pane to the left; alt+cmd+right focuses the pane to the right; alt+cmd+up focuses the pane above; alt+cmd+down focuses the pane below; alt+shift+cmd+left moves the pane left; alt+shift+cmd+right moves the pane right; alt+shift+cmd+up moves the pane up; alt+shift+cmd+down moves the pane down; cmd+] focuses the next pane; cmd+[ focuses the previous pane; shift+cmd+enter zooms the pane; alt+cmd+enter floats the pane over the layout; alt+cmd+m minimizes the floating window, or shows it again; alt+shift+cmd+enter minimizes every floating window, or shows them all again; ctrl+cmd+i inserts a path; cmd+backspace clears the input line in the shell; cmd+left moves to the start of the line in the shell; cmd+right moves to the end of the line in the shell; alt+left moves a word left in the shell; alt+right moves a word right in the shell; cmd+up jumps to the previous shell prompt; cmd+down jumps to the next shell prompt; cmd+f opens find; cmd+g finds the next match; shift+cmd+g finds the previous match while find is open; shift+cmd+= increases the font size; cmd+= increases the font size; cmd+- decreases the font size; cmd+[Digit0] resets the font size; cmd+/ toggles the sidebar; cmd+. toggles the activity sidebar; shift+cmd+s toggles the tab style.
- Never bind macOS system shortcuts: cmd+q, cmd+h, cmd+m, cmd+tab, cmd+space,
  cmd+shift+3, cmd+shift+4, cmd+shift+5, and ctrl+cmd+q. A source line on one of them,
  whatever it does, gets no rex.bind and goes under "Could not migrate" with the reason
  "macOS uses this key itself". Check every key you are about to bind against this list,
  in any modifier order (`shift+cmd+5` is cmd+shift+5), and after expanding a source's
  own modifier name such as kitty_mod or a leader.
- Where a source binding has no Rex action, do not approximate it with something
  different. Leave it out and report it.

## Herdr
The prefix is ctrl+b: a binding written `prefix+n` is the sequence
`ctrl+b>n`, and one written without `prefix+` is a plain key.
The table below has every line of the file translated. Copy its lines; do not translate
them again.
- A `[[keys.command]]` key, a plugin key and a navigate-mode key are never bound in Rex,
  not even to a custom action that runs the program: leave each such key unbound. Rex's
  report lists them.
- Theme, UI and notification settings are not migrated; the table gives each its reason.

### Every Herdr binding, line by line
Rex read the files and translated and verified each line that binds a key. Write every
`rex.bind` below exactly as given, each once, and nothing else for that line. A line
marked "not written" or "already Rex's default" gets no line at all. Every line
here goes in your report under the list its marking names (see Report).
- ~/.config/herdr/config.toml:1 `onboarding = false`
  not written: The Herdr setting onboarding has no counterpart in Rex.
- ~/.config/herdr/config.toml:4 `delivery = "system"`
  not written: The Herdr setting ui.toast.delivery has no counterpart in Rex.
- ~/.config/herdr/config.toml:6 `[[keys.command]] key = "prefix+f" type = "plugin_action" command = "herdr-file-viewer.open-file-viewer"`
  not written: "open file viewer in split": a custom command that invokes the plugin action `herdr-file-viewer.open-file-viewer`; Rex has no counterpart, and the key stays unbound
- ~/.config/herdr/config.toml:12 `[[keys.command]] key = "prefix+shift+f" type = "plugin_action" command = "herdr-file-viewer.open-file-viewer-tab"`
  not written: "open file viewer in tab": a custom command that invokes the plugin action `herdr-file-viewer.open-file-viewer-tab`; Rex has no counterpart, and the key stays unbound
- ~/.config/herdr/config.toml:21 `status_indicators = "symbols"`
  not written: The Herdr setting ui.status_indicators has no counterpart in Rex.
- ~/.config/herdr/config.toml:28 `rows = [["state_icon", "workspace"]]`
  not written: The Herdr setting ui.sidebar.spaces.rows has no counterpart in Rex.
- ~/.config/herdr/config.toml:31 `name = "catppuccin"`
  not written: The theme is not migrated; Rex has its own themes in Settings.
- ~/.config/herdr/config.toml:32 `auto_switch = false`
  not written: The Herdr setting theme.auto_switch has no counterpart in Rex.

## Ghostty
- `keybind = mods+key=action` becomes `rex.bind`. The table below has every keybind line
  translated. Copy its lines; do not translate them again.
- `keybind = clear` removes Ghostty's defaults; it has no effect on Rex and needs no line.
- Do not migrate theme, font, colors, padding or window settings, and write nothing
  about them in init.lua. The table gives each such line its reason; carry it into
  your report.

### Every Ghostty binding, line by line
Rex read the files and translated and verified each line that binds a key. Write every
`rex.bind` below exactly as given, each once, and nothing else for that line. A line
marked "not written" or "already Rex's default" gets no line at all. Every line
here goes in your report under the list its marking names (see Report).
- ~/.config/ghostty/config:3 `theme = Catppuccin Mocha`
  not written: The theme is not migrated. Settings > Theme has an Import button that reads a Ghostty or iTerm theme file.
- ~/.config/ghostty/config:9 `bell-features = system,audio`
  not written: The Ghostty setting bell-features has no counterpart in Rex.

## iTerm2
- The settings are a binary property list. Read them with
  `plutil -convert json -o - <path>` or `defaults export com.googlecode.iterm2 -`, and
  look only at `GlobalKeyMap`, each profile's `Keyboard Map` under `New Bookmarks`, and
  `Hotkey` settings. Ignore everything else in the file.
- Each entry's key is "<keycode>-<modifier flags>" in hexadecimal: the keycode is the
  character the key types (`0x63` is c, `0x7d` is `}`, which is shift and `]`), or an
  arrow (`0xf700` up, `0xf701` down, `0xf702` left, `0xf703` right). The modifier flags
  are macOS NSEvent values added together: shift 0x20000, control 0x40000, option
  0x80000, command 0x100000. So `0x120000` is shift+cmd, `0x140000` is ctrl+cmd,
  `0x180000` is alt+cmd, `0x1a0000` is alt+shift+cmd, and `0xa0000` is alt+shift. Keep
  every flag: `0xf702-0x180000` is `alt+cmd+left`, not `alt+left`. Write the Rex key
  unshifted: `0x7d-0x120000` is `shift+cmd+]`.
- Each entry's `Action` is a number from iTerm2's source, where "window" means a tab and
  "session" means a pane: 0 next pane, 1 next tab, 2 previous pane, 3 previous tab,
  10 escape sequence, 11 hex code, 12 text, 13 ignore, 18 select pane left (pane.focus
  left), 19 select pane right (pane.focus right), 20 select pane above (pane.focus up),
  21 select pane below (pane.focus down), 23 toggle full screen, 25 select menu item,
  26 new window with profile,
  27 new tab with profile, 28 split horizontally (one pane above the other), 29 split
  vertically (side by side), 30 next pane, 31 previous pane, 33 and 34 move tab left and
  right, 35 run coprocess, 36 find, 49 to 52 resize the pane, 53 to 56 swap panes,
  63 send snippet, 66 sequence, 73 copy mode. `Text` carries the profile GUID, the text,
  the hex bytes or the command. Report any number not listed.
- iTerm2 actions map as follows. New tab with profile: client.tab.new; next and previous
  tab: client.tab.next and client.tab.previous; move tab left and right: client.tab.move
  with direction backward and forward; split vertically: pane.split with direction right;
  split horizontally: pane.split with direction down; select pane 18 to 21: pane.focus
  with the direction given above, and the full modifier set of the entry's key (an
  `0x180000` entry keeps both alt and cmd); next and previous pane: pane.focus_next and
  pane.focus_previous; swap pane: pane.move with the direction; resize: pane.resize with
  the direction; new window with profile: client.window.new; toggle full screen:
  client.window.fullscreen.toggle; find: client.find.open; hex code and text of one
  key: pane.send_key with that key (`0x0c` is ctrl+l); longer text, escape sequences,
  select menu item, run coprocess, snippets, sequences, copy mode, scrolling and the
  hotkey window: no counterpart, report them with the entry's key and action number.
- Do not migrate profiles, fonts, colors or badges. Say so in the report.

## Conflicts between sources
Rex compared only the sources with tables. After reading the iTerm2 file,
collect every key that more than one source binds, and ask me once per pair of sources, naming the keys, for example:
"kitty and zellij both bind 2 keys (alt+t, alt+x). Keep kitty's for all, keep zellij's for
all, or choose per key?" Ask per key only when I choose per key. Wait for my answers, and
never decide a conflict yourself. If no key is shared, say so and ask nothing.
A source is one program, with every file it loads: a tmux.conf and the file it sources, or
a Ghostty config and its config-file includes, are one source, and inside one source the
line the program loads last wins, as it does in the program itself. That is not a conflict
and not a question. Write exactly one binding for each such key, never two lines that
leave the last one to win. Rex's own defaults are not conflicts: a source binding on a
default key replaces the default and is listed under "Replaced Rex defaults".

## Check your work
Run these commands exactly as written, paths and all: your shell may lack the Rex
terminal's environment, and a bare `rex` could be another Rex.
1. Run `REX_CONFIG='/Users/jds/.config/rex/init.lua' '/Users/jds/Library/Application Support/com.superlogical.rex/RexServer/Versions/1758/Rex Server.app/Contents/MacOS/rex' config check`. It must exit 0 and print no error or warning lines.
   Fix the file and run it again until it does.
2. Compare the file with the tables above, line by line: every `rex.bind` marked "write" is
   in the file exactly as given, each once, and nothing is written for a line marked "not
   written" or "already Rex's default". Fix the file until every binding is in place.
3. Run `'/Users/jds/Library/Application Support/com.superlogical.rex/RexServer/Versions/1758/Rex Server.app/Contents/MacOS/rex' -S 'unix:///Users/jds/Library/Application%20Support/rex/server.sock' config reload` once. Do not ask me before reloading: this migration is
   what I asked for, and nothing is active until the reload. If it fails with "operation
   not permitted" or cannot connect, your sandbox blocked it: do not retry it and do not
   work around it. If you can ask me to approve running a command outside your sandbox,
   ask once, the way you normally do, and run it again on approval. Otherwise tell me in
   one line: "Your agent's sandbox blocked reloading Rex. Choose Reload Config in Rex."
   In the report's checks, say the reload is pending, not failed.
4. After a reload that worked, run `'/Users/jds/Library/Application Support/com.superlogical.rex/RexServer/Versions/1758/Rex Server.app/Contents/MacOS/rex' -S 'unix:///Users/jds/Library/Application%20Support/rex/server.sock' keymap --json`. Its diagnostics list must be
   empty; fix the file, reload and check again until it is. If this fails the way the
   reload did, say so in one line and rely on the checks above.

## Report
Keep it short. Do not print the file, the diff, or any command output.
Give the path of the file, then four lists in this order, one line per entry, then the
result of each check in one line: config check, reload, keymap.
For every line in the tables above, the table says which list it goes in: a line you
wrote goes under "Migrated"; a line marked "already Rex's default" goes under
"Migrated" with "(Rex default)"; a line marked "(replaces a Rex default)" also goes
under "Replaced Rex defaults", in words; a line marked "loses to" goes under
"Conflicts between sources"; and any other line marked "not written" goes under "Could
not migrate" with the reason the table gives. Quote each source line as the table does,
with its file and line number, and leave none out.
- Migrated: each source line, the Rex key it became, and the action. A line that was
  already Rex's default is listed here with "(Rex default)".
- Replaced Rex defaults: one line per replaced default, in words: what the key no longer
  does, and what it does now and the line that won. Nothing else goes here.
- Conflicts between sources: each key more than one source bound, which source won, and
  the losing line verbatim.
- Could not migrate: each source binding or setting that has no counterpart, with the
  original line and one sentence on why. Settings are lines too: list each theme, font,
  color, opacity, import or include line on its own, quoted as written with its file and
  line number, never summarised together as "fonts and colors".
Never drop a binding silently. If it is not in the first list, it must be in the third or
the fourth.
