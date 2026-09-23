#!/usr/bin/env python3
"""Rank Claude Code sessions by how much real work happened in them.

Wall-clock span is mostly noise: a session left open overnight scores huge.
"Active time" sums the gaps between consecutive events and drops any gap
longer than a threshold, so idle time doesn't count.

Token counts come straight from each assistant record's usage block. "total"
is every token billed against the context: fresh input + cache writes + cache
reads + output. Cache reads dominate, because each turn re-reads the whole
conversation.

Two counting traps this handles:
  - Tool results arrive as type "user" records, so raw user counts are ~20x
    the real number of things you typed. Human prompts are distinct promptIds.
  - A resumed session replays its parent's history under a NEW sessionId, so
    the child inherits the parent's start time. Events are attributed to the
    sessionId that first recorded them.

Usage: session-length.py [--top N] [--sort active5|active15|span|prompts]
"""
import json, glob, argparse, collections, datetime as dt

PROJECTS = '/Users/jds/.claude/projects/*/*.jsonl'


def load():
    """Return {session_id: {key: event}} with replayed history stripped.

    An event whose uuid was already claimed by another sessionId belongs to
    that earlier session -- it is only present here because the session was
    resumed. Attributing it to the child would give the child its parent's
    start time and an inflated span.
    """
    sessions = collections.defaultdict(dict)   # sid -> key -> event
    untimed = collections.defaultdict(dict)    # sid -> field -> last value
    files = collections.defaultdict(set)
    owner = {}                                 # uuid -> sid that first recorded it
    records = []

    for path in sorted(glob.glob(PROJECTS)):
        for line in open(path, errors='ignore'):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            sid = d.get('sessionId')
            if not sid:
                continue
            files[sid].add(path)
            if d.get('type') == 'ai-title':
                untimed[sid]['title'] = d.get('aiTitle')
            if 'timestamp' in d:
                records.append((d['timestamp'], sid, d, line))

    # Earliest timestamp wins the uuid, so the original session keeps its events.
    for _, sid, d, line in sorted(records, key=lambda r: r[0]):
        uuid = d.get('uuid')
        if uuid:
            if uuid in owner and owner[uuid] != sid:
                continue          # replayed into a resumed session; skip
            owner[uuid] = sid
        sessions[sid][uuid or line] = d
    return sessions, untimed, files


def active_time(times, cutoff_s):
    """Sum consecutive gaps, ignoring any gap longer than cutoff."""
    total = 0.0
    for a, b in zip(times, times[1:]):
        gap = (b - a).total_seconds()
        if 0 <= gap <= cutoff_s:
            total += gap
    return total


def analyze(sid, events, meta, paths):
    ts = lambda e: dt.datetime.fromisoformat(e['timestamp'].replace('Z', '+00:00'))
    events = sorted(events.values(), key=ts)
    times = [ts(e) for e in events]

    main = [e for e in events if not e.get('isSidechain')]
    gaps = [(b - a).total_seconds() for a, b in zip(times, times[1:])] or [0]

    tok = collections.Counter()
    per_model = collections.defaultdict(collections.Counter)
    for e in events:
        if e.get('type') != 'assistant':
            continue
        msg = e.get('message')
        if not isinstance(msg, dict):
            continue
        u = msg.get('usage')
        if not isinstance(u, dict):
            continue
        counts = {
            'input': u.get('input_tokens', 0) or 0,
            'cache_write': u.get('cache_creation_input_tokens', 0) or 0,
            'cache_read': u.get('cache_read_input_tokens', 0) or 0,
            'output': u.get('output_tokens', 0) or 0,
        }
        counts['total'] = sum(counts.values())
        tok.update(counts)
        model = msg.get('model') or 'unknown'
        per_model[model].update(counts)

    return {
        'sid': sid,
        'title': meta.get('title') or '(untitled)',
        'span': (times[-1] - times[0]).total_seconds(),
        'active5': active_time(times, 300),
        'active15': active_time(times, 900),
        # Distinct promptId == things you actually typed. Bare user records
        # are mostly tool results coming back, so they measure tool traffic.
        'prompts': len({e['promptId'] for e in main
                        if e.get('type') == 'user' and not e.get('isMeta')
                        and e.get('promptId')}),
        'toolres': sum(1 for e in main
                       if e.get('type') == 'user' and not e.get('isMeta')),
        'replies': sum(1 for e in main if e.get('type') == 'assistant'),
        'planned': any(e.get('permissionMode') == 'plan' for e in events),
        'max_gap': max(gaps),
        'start': times[0],
        'cwd': next((e['cwd'] for e in reversed(events) if e.get('cwd')), '?'),
        'branch': next((e['gitBranch'] for e in reversed(events) if e.get('gitBranch')), ''),
        'files': len(paths),
        'path': sorted(paths)[0],
        'tok': tok,
        'per_model': per_model,
    }


def tk(n):
    """Tokens, abbreviated: 1.2M / 340K / 512."""
    if n >= 1_000_000:
        return f'{n / 1_000_000:.1f}M'
    if n >= 1_000:
        return f'{n / 1_000:.0f}K'
    return str(n)


def hm(seconds):
    h, m = divmod(int(seconds) // 60, 60)
    return f'{h}h{m:02d}m' if h else f'{m}m'


EPILOG = """\
How duration is measured
  Wall-clock span is misleading: a session left open overnight scores huge.
  "Active" time instead walks the session's events in order, sums the gap
  between each consecutive pair, and DISCARDS any gap longer than a cutoff --
  so idle time is not counted.

    active5     gaps over 5 minutes dropped. Counts only stretches where
                something happened at least every 5 min. The strict number.
    active15    same, 15-minute cutoff. More forgiving of thinking/reading
                pauses, so it is always >= active5.

  If a session ranks the same under both, the ranking is not an artifact of
  where the cutoff was drawn. Pick active5 for "hands on keyboard", active15
  for "engaged with the problem".

TIME columns
  span        last event minus first, idle included -- the naive number.
  idle-max    longest single gap. A big value means it sat open (e.g.
              overnight) and span is mostly nothing.
  prompts     distinct promptIds = things you actually typed. Tool results
              are recorded as "user" records too, so a raw user count is
              ~20x too high; this counts only real prompts.
  toolres     tool results returned. prompts vs toolres shows how autonomous
              a session was: 14 prompts to 449 tool results is hands-off.
  replies     assistant messages.
  plan        "yes" if the session ever entered plan mode -- the spec-then-
              execute arc.

TOKENS columns
  total       input + cache-w + cache-r + output, i.e. everything billed
              against the context.
  input       fresh (uncached) input tokens.
  cache-w     written to the cache.
  cache-r     read from the cache. This dominates everything: each turn
              re-reads the whole conversation, so tokens grow with the
              square of the turn count, not linearly.
  output      tokens the model generated -- the best proxy for work produced.
  share       this model's percent of the session total. A session using
              more than one model gets one row per model plus a
              "= session total" line.

Notes
  Sessions are read from ~/.claude/projects, so this covers only this
  machine, and old transcripts may have been pruned. A resumed session
  replays its parent's history under a new sessionId; those events are
  credited to the session that recorded them first, so spans are not
  inflated. "<synthetic>" is Claude Code's placeholder for locally
  generated messages, not a real model.

Examples
  session-length.py                        top 15 by active5
  session-length.py --top 5 --projects 5   shorter report
  session-length.py --sort tokens          rank by token count
  session-length.py --sort span            rank by wall-clock (inflated)
"""


def main():
    ap = argparse.ArgumentParser(
        description='Rank Claude Code sessions by how much real work happened '
                    'in them, ignoring time the session sat idle.',
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--top', type=int, default=15, metavar='N',
                    help='sessions to show in each table (default 15)')
    ap.add_argument('--projects', type=int, default=5, metavar='N',
                    help='projects in the rollup at the bottom (default 5)')
    ap.add_argument('--sort', default='active5',
                    choices=['active5', 'active15', 'span', 'prompts', 'tokens'],
                    help='ranking metric, applied to both tables '
                         '(default active5)')
    args = ap.parse_args()

    sessions, untimed, files = load()
    rows = [analyze(sid, ev, untimed.get(sid, {}), files[sid])
            for sid, ev in sessions.items() if ev]
    key = (lambda r: r['tok']['total']) if args.sort == 'tokens' \
        else (lambda r: r[args.sort])
    rows.sort(key=key, reverse=True)

    print(f'{len(rows)} sessions. Ranked by {args.sort}. '
          '"active" drops idle gaps over 5/15 min.')

    print('\nTIME')
    hdr = (f'{"":>3} {"active5":>8} {"active15":>8} {"span":>8} {"idle-max":>8} '
           f'{"prompts":>7} {"toolres":>7} {"replies":>7} {"plan":>4}  {"date":<10} title')
    print(hdr)
    print('-' * len(hdr))
    for i, r in enumerate(rows[:args.top], 1):
        print(f'{i:>3} {hm(r["active5"]):>8} {hm(r["active15"]):>8} {hm(r["span"]):>8} '
              f'{hm(r["max_gap"]):>8} {r["prompts"]:>7} {r["toolres"]:>7} {r["replies"]:>7} '
              f'{"yes" if r["planned"] else "":>4}  '
              f'{r["start"].astimezone().date()}  {r["title"][:52]}')

    print('\nTOKENS')
    thdr = (f'{"":>3} {"model":<26} {"total":>8} {"input":>7} {"cache-w":>8} '
            f'{"cache-r":>8} {"output":>7} {"share":>6}  title')
    print(thdr)
    print('-' * len(thdr))
    for i, r in enumerate(rows[:args.top], 1):
        models = sorted(r['per_model'].items(), key=lambda kv: -kv[1]['total'])
        for n, (model, c) in enumerate(models):
            share = 100 * c['total'] / r['tok']['total'] if r['tok']['total'] else 0
            # Rank and title print once per session, on its first model row.
            print(f'{i if n == 0 else "":>3} {model:<26} {tk(c["total"]):>8} '
                  f'{tk(c["input"]):>7} {tk(c["cache_write"]):>8} {tk(c["cache_read"]):>8} '
                  f'{tk(c["output"]):>7} {share:5.0f}%  '
                  f'{r["title"][:42] if n == 0 else ""}')
        if len(models) > 1:
            t = r['tok']
            print(f'{"":>3} {"= session total":<26} {tk(t["total"]):>8} '
                  f'{tk(t["input"]):>7} {tk(t["cache_write"]):>8} {tk(t["cache_read"]):>8} '
                  f'{tk(t["output"]):>7} {100:5.0f}%')

    print('\nDetail:')
    for i, r in enumerate(rows[:args.top], 1):
        print(f'{i:>3}. {r["title"][:60]}')
        print(f'     {r["cwd"]}' + (f'  [{r["branch"]}]' if r['branch'] else ''))
        print(f'     {r["path"]}' + (f'   ({r["files"]} files — resumed)' if r['files'] > 1 else ''))

    tot5 = sum(r['active5'] for r in rows)
    print(f'\nTotals: {hm(tot5)} active (5min) across all sessions; '
          f'{hm(sum(r["span"] for r in rows))} of wall-clock span.')
    print(f'Sessions that used plan mode: {sum(1 for r in rows if r["planned"])}')

    grand = collections.Counter()
    by_model = collections.defaultdict(collections.Counter)
    by_project = collections.defaultdict(collections.Counter)
    proj_sessions = collections.Counter()
    for r in rows:
        grand.update(r['tok'])
        for model, counts in r['per_model'].items():
            by_model[model].update(counts)
        by_project[r['cwd']].update(r['tok'])
        proj_sessions[r['cwd']] += 1

    print(f'\nTokens: {tk(grand["total"])} total = '
          f'{tk(grand["input"])} fresh input + {tk(grand["cache_write"])} cache write + '
          f'{tk(grand["cache_read"])} cache read + {tk(grand["output"])} output')

    print('\nBy model:')
    print(f'  {"model":<28} {"total":>8} {"input":>8} {"cache-w":>8} {"cache-r":>8} {"output":>8}')
    for model, c in sorted(by_model.items(), key=lambda kv: -kv[1]['total']):
        print(f'  {model:<28} {tk(c["total"]):>8} {tk(c["input"]):>8} '
              f'{tk(c["cache_write"]):>8} {tk(c["cache_read"]):>8} {tk(c["output"]):>8}')

    print(f'\nTop {args.projects} projects by tokens:')
    print(f'  {"":>3} {"total":>8} {"output":>8} {"sessions":>8}  project')
    top = sorted(by_project.items(), key=lambda kv: -kv[1]['total'])[:args.projects]
    for i, (proj, c) in enumerate(top, 1):
        print(f'  {i:>3} {tk(c["total"]):>8} {tk(c["output"]):>8} '
              f'{proj_sessions[proj]:>8}  {proj}')


if __name__ == '__main__':
    main()
