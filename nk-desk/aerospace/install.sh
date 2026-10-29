#!/bin/bash
# Wire this checkout into AeroSpace. Safe to re-run.
#   - symlinks organize.py and its tests into ~/.config/aerospace
#   - builds the teleprompter tool
#   - seeds ~/.config/desk/rules.json from the example if you have none
#   - writes ~/.aerospace.toml from the template if you have none
#     (organize.py rewrites its ultrawide gaps, so it is a copy, not a link)
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
dest="$HOME/.config/aerospace"
rules="$HOME/.config/desk/rules.json"
mkdir -p "$dest" "$(dirname "$rules")"

for f in organize.py test_organize.py rules.example.json teleprompter.swift; do
  ln -sf "$here/$f" "$dest/$f"
done
swiftc -O "$here/teleprompter.swift" -o "$dest/teleprompter"

[ -f "$rules" ] || cp "$here/rules.example.json" "$rules"

if [ ! -f "$HOME/.aerospace.toml" ]; then
  ultra="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("ultrawide","secondary"))' "$rules")"
  prompter="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("prompter","none"))' "$rules")"
  sed -e "s/ULTRA/$ultra/g" -e "s/PROMPTER/$prompter/g" "$here/aerospace.toml" > "$HOME/.aerospace.toml"
fi

(cd "$dest" && python3 -m unittest test_organize)
echo "installed; reload with: aerospace reload-config"
