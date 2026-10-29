#!/usr/bin/env python3
"""Sort windows onto task workspaces, keep the ultrawide centered, log usage.

Runs on every focus change (see ~/.aerospace.toml). Three jobs:

1. Sort. AeroSpace's on-window-detected rules only see bundle id and title.
   A second Chrome instance (say a CAC-only profile) and the agent Chrome are separate Chrome
   instances with one profile each, so their titles carry no profile suffix
   and look identical. The instance is only visible in the process's
   --user-data-dir, so this script reads that. Only windows not seen before
   are moved, so a window you put somewhere by hand stays put. --all
   re-sorts everything.

2. Center. No window may span the full ultrawide. The side gap on that
   monitor shrinks as tiled windows are added (margin_for), applied by
   rewriting the gap in ~/.aerospace.toml and reloading.

3. Log. Every placement change and every focus change goes to LOG as one
   JSON line, tagged by="sorter" when this script moved it and by="user"
   otherwise. learn.py turns that into dwell time per app per workspace.
"""
import fcntl
import json
import os
import re
import subprocess
import sys
import time

STATE = os.path.expanduser("~/.cache/aerospace-organize-state.json")
LOG = os.path.expanduser("~/.local/state/aerospace/usage.jsonl")
CONFIG = os.path.expanduser("~/.aerospace.toml")
# exec-and-forget runs with a bare PATH that lacks Homebrew.
AEROSPACE = "/opt/homebrew/bin/aerospace"

# Personal rules (which app or Chrome profile pins to which workspace) live in
# RULES, outside the repo. See rules.example.json. M is the laptop display.
RULES = os.path.expanduser("~/.config/desk/rules.json")


def load_rules(path=RULES):
    try:
        return json.load(open(path))
    except (OSError, ValueError):
        return {}


_r = load_rules()
ULTRAWIDE = _r.get("ultrawide", "")
# Teleprompter monitor name. When it is connected, calls go to workspace T on it
# so the faces sit behind the camera lens; otherwise they go to the laptop (M).
PROMPTER = _r.get("prompter", "")
APPS = _r.get("apps", {})
CHROME_DATA_DIRS = _r.get("chrome_data_dirs", {})
CHROME_PROFILES = _r.get("chrome_profiles", {})
# Launcher windows that park somewhere while the app's other windows stay put,
# e.g. Windows App's connection center vs. the remote desktop it opens.
LAUNCHER_TITLES = _r.get("launcher_titles", {})
GHOSTTY = "com.mitchellh.ghostty"
SESSIONS = [str(i) for i in range(1, 10)]
CHROME = "com.google.Chrome"
CALENDAR = re.compile(r"^Google Calendar| - Calendar - ")
# Call windows in any Chrome instance go to the laptop. Pop a Teams meeting out
# to its own window and it lands there.
MEETING = re.compile(r"^Meet - |Microsoft Teams|Webex|^Zoom ")


def window_key(bundle, cmdline, title):
    """Stable name for 'what kind of window this is', used for rules and logs."""
    if bundle != CHROME:
        return bundle
    if CALENDAR.search(title):
        return "chrome:calendar"
    if MEETING.search(title):
        return "chrome:meeting"
    for data_dir in CHROME_DATA_DIRS:
        if f"/Google/{data_dir} " in cmdline + " ":
            return f"chrome:{data_dir}"
    for profile in CHROME_PROFILES:
        if title.endswith(f"- Google Chrome - {profile}"):
            return f"chrome:{profile}"
    return "chrome:other"


def classify(bundle, cmdline, title):
    key = window_key(bundle, cmdline, title)
    if key in ("chrome:meeting", "chrome:calendar"):
        return "M"
    if key.startswith("chrome:"):
        name = key[len("chrome:"):]
        return CHROME_DATA_DIRS.get(name) or CHROME_PROFILES.get(name)
    if bundle in LAUNCHER_TITLES:
        return LAUNCHER_TITLES[bundle].get(title)
    return APPS.get(bundle)


def call_workspace(monitor_names):
    return "T" if PROMPTER and PROMPTER in monitor_names else "M"


SIDE, CENTER = 1280, 2560  # ultrawide columns: 1280 | 2560 | 1280


def plan(n, has_ghostty):
    """n tiled windows on the visible ultrawide workspace.

    Returns (left_margin, right_margin, ghostty_moves). Ghostty owns the center
    column when there are three windows. A lone window is centered at 2560;
    with two or more there is no margin, so no space goes unused and no
    window spans the full ultrawide. Moves are
    relative to the left edge rather than to the current order, because
    list-windows does not report windows in screen order.
    """
    if n <= 1:
        return SIDE, SIDE, []
    if not has_ghostty:
        return 8, 8, []
    if n == 2:
        return 8, 8, ["left"]
    if n == 3:
        return 8, 8, ["left", "left", "right"]
    return 8, 8, []


def set_margins(cfg, left, right):
    for side, n in (("left", left), ("right", right)):
        cfg = re.sub(rf"(outer\.{side} = \[\{{ monitor\.'{ULTRAWIDE}' = )\d+", rf"\g<1>{n}", cfg)
    return cfg


def aerospace(*args):
    return subprocess.run([AEROSPACE, *args], capture_output=True, text=True).stdout


def cmdline(pid):
    return subprocess.run(["ps", "-o", "command=", "-ww", "-p", pid], capture_output=True, text=True).stdout


def log(event):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a") as f:
        f.write(json.dumps({"t": round(time.time()), **event}) + "\n")


def main():
    sweep_all = "--all" in sys.argv
    # Focus events fire in bursts; overlapping runs would double-move and double-log.
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    lock = open(STATE + ".lock", "w")
    fcntl.flock(lock, fcntl.LOCK_EX)
    try:
        state = json.load(open(STATE))
    except (OSError, ValueError):
        state = {}
    fmt = ("%{window-id}\t%{app-bundle-id}\t%{app-pid}\t%{workspace}\t%{monitor-name}\t"
           "%{workspace-is-visible}\t%{window-layout}\t%{window-title}")
    rows = [(line.split("\t", 7) + [""] * 8)[:8]
            for line in aerospace("list-windows", "--all", "--format", fmt).splitlines()]
    occupied = {r[3] for r in rows}
    call_ws = call_workspace(aerospace("list-monitors", "--format", "%{monitor-name}").splitlines())
    cmdlines = {}
    windows = {}
    for wid, bundle, pid, ws, monitor, visible, layout, title in rows:
        if bundle == CHROME and pid not in cmdlines:
            cmdlines[pid] = cmdline(pid)
        cl = cmdlines.get(pid, "")
        key = window_key(bundle, cl, title)
        prev = state.get("windows", {}).get(wid)
        target = None
        if prev is None or sweep_all:
            target = classify(bundle, cl, title)
            if key == "chrome:meeting":
                target = call_ws
            # A second Ghostty window is a new agent session: give it its own workspace.
            if (bundle == GHOSTTY and prev is None and not sweep_all and state
                    and any(r[1] == GHOSTTY and r[3] == ws and r[0] != wid for r in rows)):
                target = next((w for w in SESSIONS if w not in occupied), None)
        if target and target != ws:
            aerospace("move-node-to-workspace", "--window-id", wid, target)
            log({"ev": "place", "key": key, "from": ws, "to": target, "by": "sorter"})
            occupied.add(target)
            if bundle == GHOSTTY:
                aerospace("workspace", target)
            ws, visible = target, "false"
        elif prev is None:
            log({"ev": "place", "key": key, "from": None, "to": ws, "by": "open"})
        elif key == "chrome:meeting" and prev["key"] != "chrome:meeting" and ws != call_ws:
            # A tab in an existing window just turned into a call: send it to the
            # call screen once. If you move it back, it stays (key no longer changes).
            aerospace("move-node-to-workspace", "--window-id", wid, call_ws)
            aerospace("focus", "--window-id", wid)
            log({"ev": "place", "key": key, "from": ws, "to": call_ws, "by": "sorter"})
            ws, visible = call_ws, "false"
        elif prev["ws"] != ws:
            log({"ev": "place", "key": key, "from": prev["ws"], "to": ws, "by": "user"})
        windows[wid] = {"ws": ws, "key": key, "ultra": monitor == ULTRAWIDE and visible == "true"
                        and layout != "floating", "ghostty": bundle == GHOSTTY}

    focused = aerospace("list-windows", "--focused", "--format", "%{window-id}").strip()
    if focused in windows and focused != state.get("focused"):
        log({"ev": "focus", "key": windows[focused]["key"], "ws": windows[focused]["ws"]})

    # Laptop workspace M: accordion, re-applied when its window set changes.
    layouts = state.get("layouts", {})
    on_m = sorted(w for w, v in windows.items() if v["ws"] == "M")
    if on_m and layouts.get("M") != on_m:
        layouts["M"] = on_m
        aerospace("flatten-workspace-tree", "--workspace", "M")
        aerospace("layout", "--workspace", "M", "--root", "h_accordion")
        meeting = next((w for w in on_m if windows[w]["key"] == "chrome:meeting"), None)
        if meeting:
            aerospace("focus", "--window-id", meeting)

    # Lay out the visible ultrawide workspace, but only when its window set
    # changed, so a resize you made by hand survives.
    ultra = [(w, v) for w, v in windows.items() if v["ultra"]]
    if ultra:
        ws = ultra[0][1]["ws"]
        sig = sorted(w for w, _ in ultra)
        if layouts.get(ws) != sig:
            layouts[ws] = sig
            aerospace("flatten-workspace-tree", "--workspace", ws)
            # "auto" orientation can come up vertical; the ultrawide is always columns.
            aerospace("layout", "--workspace", ws, "--root", "h_tiles")
            tiled = [w for w, v in ultra]
            ghost = next((w for w in tiled if windows[w]["ghostty"]), None)
            left, right, moves = plan(len(tiled), ghost is not None)
            cfg = open(CONFIG).read()
            want = set_margins(cfg, left, right)
            if want != cfg:
                open(CONFIG, "w").write(want)
                aerospace("reload-config")
            for direction in moves:
                aerospace("move", "--window-id", ghost, "--boundaries", "workspace",
                          "--boundaries-action", "stop", direction)
            aerospace("balance-sizes", "--workspace", ws)
            if ghost and moves:
                aerospace("resize", "--window-id", ghost, "width", str(CENTER))

    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump({"windows": windows, "focused": focused, "layouts": layouts}, open(STATE, "w"))


if __name__ == "__main__":
    main()
