# Record a PR demo video of a Chrome window on Omarchy, hands free

Omarchy 4.x, Hyprland 0.56, gpu-screen-recorder 6.1, gh 2.103.

I verify features by letting Claude Code drive Chrome through claude-in-chrome.
Once it works I want a short mp4 of the same steps on the GitHub PR, without
me clicking a region picker or editing video. The pieces were all already on
the machine; the script that strings them together lives in
`jds_config_omarchy/bin/pr-record` (`make deploy` symlinks it into `~/bin`).

## What Omarchy already gives you

`omarchy screenrecord` (`omarchy-capture-screenrecording`) wraps
gpu-screen-recorder: H.264/HEVC mp4 into `~/Videos`, run again to stop. It is
interactive by default (slurp picker), but `--fullscreen` is not, and the
underlying `gpu-screen-recorder -w region -region WxH+X+Y` takes the same
logical coordinates that `hyprctl clients -j` reports in `at` and `size`.
So "record just the Chrome window" is a jq one-liner away.

## The workflow

```bash
pr-record start --title jds.local.me   # focus that Chrome window, record its region
# ... Claude runs the steps through claude-in-chrome ...
pr-record stop                          # stop, pack, print ~/Videos/pr-record-<ts>.mp4
pr-record attach 1234                   # gh pr comment --attach the packed file
```

`start` picks the most recently focused window of class `google-chrome`
(narrow it with `--title`), switches to its workspace, and records at 30 fps
with no cursor. `--fullscreen` records the focused monitor instead.

## Things that were not obvious

**Hyprland 0.56 dispatches in Lua.** `hyprctl dispatch focuswindow address:0x..`
now fails with "')' expected". The working form is

```bash
hyprctl eval 'return hl.dispatch(hl.dsp.focus({ window = "address:0x55a02e6972c0" }))'
```

and the error exit code is swallowed inside `$(...)` in an array assignment, so
check the result (`ok`) and re-read `hyprctl activewindow` before trusting it.
The first version of the script recorded the wrong Chrome window because of this.

**Claude-driven steps have dead air.** Every browser tool call is a few seconds
apart, so the raw recording is mostly a still image. Instead of speeding the
whole thing up, drop the frames that do not change:

```bash
ffmpeg -i raw.mp4 \
  -vf "mpdecimate=max=14,setpts=N/FRAME_RATE/TB,scale=1280:-2" \
  -r 30 -c:v libx264 -crf 28 -preset slow -pix_fmt yuv420p -movflags +faststart -an out.mp4
```

`mpdecimate` drops frames identical to the previous one; `max=14` keeps every
15th idle frame so a pause still reads as a pause (5 s becomes a third of a
second). `setpts` re-times what survives to a steady 30 fps. A 12 s idle
capture packed down to 0.8 s and 49 KB; a real 2 minute walkthrough lands
around 1 to 3 MB at 1280 wide.

**GitHub limits.** Images and GIFs max 10 MB. Video is 10 MB on free repos and
100 MB on paid org repos, H.264 recommended, mp4/mov/webm accepted. The script
warns above 10 MB. `gh pr comment --attach` and `gh pr edit --attach` upload
and embed the player, no drag and drop needed.

**No pointer in the video.** claude-in-chrome clicks without moving the real
cursor, so an mp4 shows no pointer. The extension's own `gif_creator` tool
draws click markers and action labels, which can be clearer for a 15 second
clip, but GIF is a poor fit for anything approaching 2 minutes.

**`((i++))` under `set -e`.** Post-increment from 0 evaluates to 0, which is a
non-zero exit status, which aborts the script. Use `i=$((i + 1))`.
