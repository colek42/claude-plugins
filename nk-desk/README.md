# NK Desk Plugin

AeroSpace setup for a laptop plus a 32:9 ultrawide and an optional teleprompter.

## What's Included

### Skills

- **desk**: covers how agents place windows, the workspace map, and what not to touch.

### aerospace/

- `aerospace.toml`: config template. `install.sh` fills in the monitor names.
- `organize.py`: runs on every focus change. It sorts new windows, centers the
  agent terminal on the ultrawide, sends calls to the laptop (or to the
  teleprompter when connected), and logs placement and focus for later layout tuning.
- `teleprompter.swift`: mirrors the laptop onto the teleprompter, or lists display roles.
- `rules.example.json`: shows the rules format. Real rules live in
  `~/.config/desk/rules.json` and never get committed.

## Layout

- **Laptop (M):** calendar column plus calls and chat in an accordion. Never switches.
- **Ultrawide (1-9):** one agent session per workspace. A lone window is centered
  at 2560pt. Three windows split as side | Ghostty | side (1280 | 2560 | 1280).
  No window ever takes the full 5120pt width.
- **Teleprompter (T):** calls go here while it is plugged in.

## Installation

```bash
/plugin marketplace add ~/claude-plugins
/plugin install nk-desk@nkennedy-personal
brew install --cask nikitabobko/tap/aerospace
./nk-desk/aerospace/install.sh
```

## Notes

The spec is the asset here. Every piece of this setup could be rebuilt from this
README and the tests in about an hour.
