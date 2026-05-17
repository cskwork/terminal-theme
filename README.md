# iterm2-wezterm-port

Port WezTerm aesthetics to iTerm2 in one command. Catppuccin Mocha palette,
JetBrains Mono Nerd Font, optional darkened background image, blinking-block
cursor, generous line spacing — all installed as an iTerm2 **Dynamic Profile**
so it loads without a restart and never clobbers your existing setup.

## What it ports from WezTerm

| WezTerm setting                          | iTerm2 equivalent applied         |
| ---------------------------------------- | --------------------------------- |
| `color_scheme = 'Catppuccin Mocha'`      | Full 16-color ANSI + bg/fg/cursor |
| `font = JetBrainsMono Nerd Font Medium`  | `JetBrainsMonoNFM-Medium 15`      |
| `default_cursor_style = BlinkingBlock`   | Box cursor, blinking on           |
| `backdrops/*` random rotation            | Single static image (configurable)|
| `cursor_blink_rate = 650`                | iTerm2 default blink              |
| Window padding (top 10, bottom 7.5)      | Vertical Spacing 1.05             |

What does **not** port (iTerm2 doesn't support it natively):
- Random backdrop rotation per launch — iTerm2 takes one static image.
- `LEADER+b/Shift+B` runtime backdrop cycling.
- Fancy semi-transparent tab bar.
- WebGPU 120fps rendering and freetype tuning.

## Install

Requirements: macOS, iTerm2, Python 3, JetBrains Mono Nerd Font Mono
(`brew install --cask font-jetbrains-mono-nerd-font`).

```bash
git clone https://github.com/cskwork/iterm2-wezterm-port
cd iterm2-wezterm-port

# Solid Catppuccin Mocha background, set as default profile
python3 make-profile.py --set-default

# Or with a darkened background image
python3 make-profile.py --backdrop ~/Pictures/dark-bg.jpg --set-default
```

Open a new iTerm2 window (`⌘N`). The profile is loaded automatically — no
restart required because Dynamic Profiles live outside the main plist.

## Customize

```bash
python3 make-profile.py --help
```

Common tweaks:

```bash
# Bigger font
python3 make-profile.py --font "JetBrainsMonoNFM-Medium 17"

# Image more visible
python3 make-profile.py --backdrop img.jpg --blend 0.65

# Image barely visible (max readability)
python3 make-profile.py --backdrop img.jpg --blend 0.95

# Different profile name
python3 make-profile.py --name "WezTerm Mocha Dim"
```

Re-run with different flags any time — the JSON is regenerated and iTerm2
picks it up immediately.

## How it works

iTerm2 reads every `*.json` in
`~/Library/Application Support/iTerm2/DynamicProfiles/` on launch and on
change. The script writes one JSON describing a single profile with a fresh
GUID. `--set-default` writes that GUID to
`com.googlecode.iterm2 Default Bookmark Guid` via `defaults write`.

Your existing iTerm2 profiles, preferences, and plist are untouched.

## Uninstall

```bash
rm ~/Library/Application\ Support/iTerm2/DynamicProfiles/wezterm-port.json
```

If it was set as default, pick a different default in
Preferences → Profiles → Other Actions → Set as Default.

## License

MIT. See [LICENSE](LICENSE).
