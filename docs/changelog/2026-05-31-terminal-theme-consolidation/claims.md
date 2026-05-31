# Claims

- `terminal-theme.py` is the canonical generator for iTerm2, WezTerm, Windows
  Terminal fragments, and PowerShell styling snippets.
- `make-profile.py` remains as the legacy iTerm2 entry point.
- `make-profile.ps1` ports the live Windows Terminal installer flow from the
  old Windows repo and now applies the Oh My Pi Titanium palette.
- `uninstall.ps1` removes new `terminal-theme` state and legacy
  `wezterm-port` action/profile markers.
- `docs/index.html` is a dependency-free landing page for the unified repo.
