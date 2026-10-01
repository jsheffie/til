# Omarchy Plugin Anatomy

Omarchy 4.0.2, Quickshell. Read from `$OMARCHY_PATH` on the machine.

The desktop is one long-running process, and almost everything you see in it is a plugin: a folder with a `manifest.json` and some QML. This note shows how a plugin is found, checked, switched on, and loaded.

Visual version with diagrams: [omarchy-plugin-anatomy.html](omarchy-plugin-anatomy.html)

- first-party: `$OMARCHY_PATH/shell/plugins/`
- yours: `~/.config/omarchy/plugins/<id>/`
- state: `~/.config/omarchy/shell.json`

## 1. One process, many plugins

`omarchy-shell` is a single Quickshell instance launched by Hyprland autostart. The bar, its widgets, the dropdown panels, fullscreen overlays, the Omarchy menu, the lock screen, the polkit dialog and headless services all run inside it. A `PluginRegistry` object scans two directories at startup, validates every manifest, and hands the rest of the shell a map of what exists and whether it is enabled.

```
 $OMARCHY_PATH/shell/plugins/  (first-party, manifest.json / *.manifest.json) --scan--+
                                                                                      v
 ~/.config/omarchy/plugins/    (third-party + your clones, <id>/manifest.json) --> PluginRegistry <--> shell.json
        ^                                                                       validate, merge, isEnabled()
        | watches (inotifywait -m -r: close_write create delete move)           rejects 3p omarchy.* ids
        | on change: hot reload that plugin                                         |
                                                       +----------------------------+-------------------+
                                                       v                            v                   v
                                                 Bar (kind: bar)            Panel loaders          Service host
                                                 omarchy.bar or a           panel/overlay/menu     kind: service,
                                                 replacement; widget        loaded on summon;      created once at
                                                 slots                      keepLoaded: true       startup
                                                                            stays mounted

 keybinds / CLI / menu --IPC (summon, toggle, call, rescanPlugins)--> omarchy-shell
```

Injected into every plugin: `omarchyPath`, `shell`, `manifest`, `pluginRegistry`, `barWidgetRegistry`. Bar widgets also get `bar`, `moduleName`, `settings`.

Both directories are scanned the same way. Only the enable rule differs: built-ins are on unless listed in `disabledPlugins[]`, third-party plugins are on only when an entry names them. Third-party ids can never claim the `omarchy.*` namespace.

## 2. What a plugin is

A directory with a `manifest.json` plus the QML it points at. Every declared kind needs a matching entry point, and every entry point must be a relative path that exists inside the folder.

```json
{
  "schemaVersion": 1,
  "id": "jds.hello",
  "name": "Hello",
  "version": "0.1.0",
  "kinds": ["bar-widget"],
  "entryPoints": { "barWidget": "Widget.qml" },
  "barWidget": {
    "displayName": "Hello", "category": "Info",
    "allowMultiple": true, "defaultSection": "right"
  }
}
```

| kind | entryPoints key | what it is | loaded when | root item exposes |
|---|---|---|---|---|
| `bar-widget` | `barWidget` | Component the active bar drops into a section | present in `bar.layout` | extends `BarWidget`; `open/close/opened` if it owns a popup |
| `bar` | `bar` | A full bar replacing `omarchy.bar` | startup, if `bar.id` selects it | receives `barConfig` |
| `panel` | `panel` | Floating window (OSD, dev gallery) | on summon | `open(payloadJson)`, `close()`, `opened` |
| `overlay` | `overlay` | Fullscreen surface (emojis, clipboard, image picker) | on summon | same as panel |
| `menu` | `menu` | Summoned menu (the Omarchy menu) | on summon | same as panel |
| `service` | `service` | Headless singleton, no UI | startup, if enabled | plain `Item` with `shell`, `manifest` |

A plugin may be several kinds at once. `omarchy.media` is a service plus a bar widget; `omarchy.menu` is a menu plus a bar widget. `keepLoaded: true` keeps a summoned surface mounted between uses.

### The bar widget contract

Extend `BarWidget` from `qs.Ui`. The bar injects `bar` (colors, font, orientation, `run()`, tooltips, popout coordination), `moduleName`, and `settings`, which is literally your inline entry from `shell.json`. `setting("format", "HH:mm")` reads one field with a fallback. A widget persists a change by calling `shell.updateEntryInline(id, entry)`, which is how a right-click on the clock makes the new format stick across restarts.

## 3. From git URL to running code

Distribution is just git. `omarchy plugin add <url>` does the following, in this order, and every gate that fails deletes the staging clone and stops. Nothing from the plugin is executed during install: no hooks, no sudo, only files, a manifest check, and one IPC bit-flip.

1. **url-check** - refuses git options (refuse on failure)
2. **warn + confirm** - unsandboxed code warning (abort on decline)
3. **git clone** - into `plugins/.add.tmp.$$`
4. **validate** - schema, paths, symlinks (`rm -rf` stage on failure)
5. **id is free?** - no clash, not `omarchy.*` (`rm -rf` stage on failure)
6. **mv to `plugins/<id>/`** - now a plain git checkout
7. **rescanPlugins** - IPC, registry re-walks
8. **enable?** - `--enable`, or a prompt (if no: enable later with `omarchy plugin enable <id>`)
9. **shell.json entry** - `bar.layout` or `plugins[]`
10. **shell loads entryPoint** - injects props, plugin runs

Once the folder is in place, saving any file under it triggers a hot reload through the inotify watcher, so the same folder is also the development loop.

### Update, clone, remove

- **update** is `git fetch`, a diff shown before anything changes, then `merge --ff-only`. Local edits block it. If the new revision fails validation it resets to `ORIG_HEAD`.
- **clone** copies a built-in into `~/.config/omarchy/plugins/<username>.<name>/`, rewrites the id, names it "My Clock", enables it, and routes calls made to the built-in id to your clone. Removing the clone restores the built-in.
- **remove** disables first, then deletes a git checkout, unlinks a symlink, or moves a hand-made folder to a timestamped backup.

## 4. Where "enabled" lives

There is one persisted file, `~/.config/omarchy/shell.json`. It records the deviation from the shipped defaults, and once it exists it is canonical: no deep-merge with defaults. Four rules decide whether a plugin is on.

| Case | Rule |
|---|---|
| Full bar (1p, 3p) | `bar.id` names the active bar. Missing or `omarchy.bar` means built-in. There is no off state; you replace a bar by enabling another. |
| Bar widget (1p, 3p) | On when an entry with its id sits in `bar.layout.left\|center\|right`. Settings are inline on that entry. `allowMultiple` permits several entries. |
| Third-party, non-widget (3p) | On when listed in `plugins[]`. Presence is the switch. |
| First-party, non-widget (1p) | On by default. Off only when listed in `disabledPlugins[]`, so a stock file with an empty `plugins[]` still summons the emoji picker. |

```json
{
  "version": 1,
  "bar": {
    "id": "omarchy.bar",
    "layout": {
      "left":   [ { "id": "omarchy.menu" }, { "id": "omarchy.workspaces" } ],
      "center": [],
      "right":  [ { "id": "omarchy.clock", "format": "h:mm AP" }, { "id": "jds.hello", "greeting": "yo" } ]
    }
  },
  "plugins": [ { "id": "acme.weather-extra" } ],
  "disabledPlugins": [ "omarchy.nightlight" ]
}
```

## 5. Talking to plugins

The shell exposes one IPC target, `shell`, and the wrapper `omarchy-shell` forwards to it. This is also how the stock keybindings work: `SUPER+CTRL+E` runs `omarchy-shell shell toggle omarchy.emojis`.

```
omarchy-shell shell listPlugins
omarchy-shell shell rescanPlugins
omarchy-shell shell summon omarchy.emojis '{}'
omarchy-shell shell toggle omarchy.clock  '{}'
omarchy-shell shell call   <id> <method> <arg>
omarchy-shell shell setPluginEnabled <id> "true"   # only the literal string "true" enables
```

Calls aimed at a built-in id are rerouted to an enabled clone, so keybindings and scripts keep working after `omarchy plugin clone`.

## 6. CLI cheat sheet

| command | does |
|---|---|
| `omarchy plugin list [--json]` | id, enabled, 1p/3p, kinds, name for every discovered plugin |
| `omarchy plugin enable <id> [--section right] [--index n]` | switch on, placing a widget on the bar |
| `omarchy plugin disable <id>` | remove from layout, or add to `disabledPlugins[]` |
| `omarchy plugin add <git-url> [--enable] [--yes]` | the flow in section 3 |
| `omarchy plugin update [<id>] [--yes]` | diff, then fast-forward; no id updates all |
| `omarchy plugin clone <omarchy.id> [--edit]` | copy a built-in into your plugins dir and switch to it |
| `omarchy plugin remove <id>` | disable, then delete / unlink / back up |
| `omarchy plugin validate <dir>` | the same checks the shell runs at load |

The same actions live in the menu under **Setup > Plugins**. Lighter than a plugin: an inline `type: "command"` or `type: "qml"` module in `bar.layout`, a hook script in `~/.config/omarchy/hooks/<event>.d/`, or a row in `extensions/omarchy-menu.jsonc`.

## Warning: no sandbox

A plugin is QML and JavaScript running inside the process that draws your bar, holds your lock screen and runs your polkit agent, with your full user privileges for the life of the session. The protections are all at install time: reserved namespace, path and symlink checks, diff-before-update, and nothing enabled until you say so. Read the code before you enable it.

## Sources

`manual/32-shell-plugins.md`, `docs/omarchy-shell.md`, `shell/README.md`, `shell/plugins/README.md`, `shell/services/PluginRegistry.qml`, `shell/shell.qml`, `shell/Ui/BarWidget.qml`, `bin/omarchy-plugin-*` (in the Omarchy install).
