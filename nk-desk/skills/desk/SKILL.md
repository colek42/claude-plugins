# Desk (window layout)

This skill covers placing windows on Cole's desk, which AeroSpace manages.

## When to Use

Activates when:
- An agent wants to show Cole something (a page, a brief, a dashboard)
- A window ended up on the wrong screen, or the layout looks wrong
- Adding or changing a rule for where an app goes
- Setting up for a call, or using the teleprompter

## The desk

| Workspace | Screen | What lives there |
|-----------|--------|------------------|
| M | laptop | calls, chat, calendar (calendar floats in a 390pt left gap) |
| 1-9 | ultrawide | one agent session each: side \| Ghostty \| side |
| N, P | ultrawide | apps pinned by `~/.config/desk/rules.json` |
| T | teleprompter | calls go here while it is connected |

`~/.config/aerospace/organize.py` runs on every focus change. It does three things:
- Sorts **new** windows. A window Cole moved by hand stays where he put it.
- Lays out a workspace only when its set of windows changes.
- Appends placement and focus events to `~/.local/state/aerospace/usage.jsonl`.

## Rules for agents

1. **Do not open windows on Cole's screens unannounced.** If the session that owns the desk is running, ask it. Otherwise, open the window and then place it yourself:
   ```bash
   aerospace list-windows --all --format '%{window-id}|%{workspace}|%{app-name}|%{window-title}'
   aerospace move-node-to-workspace --window-id <id> <workspace>
   ```
2. **Show a page next to a session.** Move it into that session's ultrawide workspace. With three windows, Ghostty takes the 2560pt center column and the others take the sides.
3. **Never move a live call off M or T.** Call windows are recognized by title (Teams, Meet, Zoom, Webex).
4. **Rules are local and personal.** Edit `~/.config/desk/rules.json`, never the repo copy. Profile names and contract details do not belong in this public repo.
5. **Chrome instances look alike.** Single-profile Chrome instances (the agent browser, a CAC-only profile) have the same window titles. `organize.py` tells them apart by `--user-data-dir` in `ps`. Window titles cannot do it.

## Checks

```bash
cd ~/.config/aerospace && python3 -m unittest test_organize   # rules and layout planner
~/.config/aerospace/organize.py --all                         # re-sort everything
~/.config/aerospace/teleprompter list                         # display roles
```

To verify a layout, read the real window frames from System Events (`position`, `size`). Don't trust the order that `aerospace list-windows` prints, because it is not screen order.
