# terminal-theme

Generate one Oh My Pi Titanium terminal theme for iTerm2, WezTerm, Windows
Terminal, Orca, and PowerShell-adjacent shell styling.

The project keeps the iTerm2 Dynamic Profile installer, then adds portable
theme fragments for terminal apps that use different config formats.

## Targets

| Target | Output |
| --- | --- |
| iTerm2 | Dynamic Profile JSON |
| WezTerm | `wezterm.lua` color scheme |
| Windows Terminal | settings fragment with a `schemes` entry |
| Orca | settings fragment with `terminalColorOverrides` |
| PowerShell | profile snippet for `$PSStyle` and `$Host.PrivateData` |

PowerShell does not own the terminal ANSI palette. Use the iTerm2, WezTerm,
Windows Terminal, or Orca target for full foreground, background, cursor,
selection, and 16-color ANSI palette support.

## Install iTerm2

Requirements: macOS, iTerm2, Python 3, JetBrains Mono Nerd Font Mono
(`brew install --cask font-jetbrains-mono-nerd-font`).

```bash
git clone https://github.com/cskwork/terminal-theme
cd terminal-theme

python3 terminal-theme.py --set-default
```

Open a new iTerm2 window. The profile is loaded automatically because Dynamic
Profiles live outside the main plist.

## Generate All Targets

```bash
python3 terminal-theme.py --target all --output-dir dist
```

This writes:

```text
dist/iterm2-dynamic-profile.json
dist/wezterm.lua
dist/windows-terminal.json
dist/orca-settings.json
dist/Microsoft.PowerShell_profile.ps1
```

## Generate One Target

```bash
python3 terminal-theme.py --target wezterm --output wezterm.lua
python3 terminal-theme.py --target windows-terminal --output windows-terminal.json
python3 terminal-theme.py --target orca --output orca-settings.json
python3 terminal-theme.py --target powershell --output Microsoft.PowerShell_profile.ps1
```

The Orca target writes the same `settings.terminalColorOverrides` shape used in
Orca's settings store, so it can be merged into an Orca settings backup or used
as the source for the terminal color controls.

The legacy entry point still works for iTerm2:

```bash
python3 make-profile.py --set-default
```

## Install Windows Terminal

Requirements: Windows Terminal, PowerShell 5.1 or later. Run from a PowerShell
prompt in this repo:

```powershell
pwsh -ExecutionPolicy Bypass -File .\make-profile.ps1
```

Optional full setup:

```powershell
pwsh -ExecutionPolicy Bypass -File .\make-profile.ps1 -InstallOhMyPosh -InstallFont
```

The installer patches the live Windows Terminal `settings.json`, creates a
timestamped backup, adds the Oh My Pi Titanium scheme, sets JetBrainsMono NFM
as the default font, configures copy/paste keybindings, and adds an idempotent
oh-my-posh block to `$PROFILE`.

Preview the planned changes without writing:

```powershell
pwsh -ExecutionPolicy Bypass -File .\make-profile.ps1 -WhatIf
```

## Customize

```bash
python3 terminal-theme.py --help
```

Common tweaks:

```bash
python3 terminal-theme.py --font "JetBrainsMonoNFM-Medium 17"
python3 terminal-theme.py --wezterm-font-size 17
python3 terminal-theme.py --backdrop ~/Pictures/dark-bg.jpg --blend 0.65
python3 terminal-theme.py --name "Terminal Theme Titanium"
```

## iTerm2 Uninstall

```bash
rm ~/Library/Application\ Support/iTerm2/DynamicProfiles/terminal-theme.json
```

If it was set as default, pick a different default in Preferences > Profiles >
Other Actions > Set as Default.

## Windows Uninstall

```powershell
pwsh -ExecutionPolicy Bypass -File .\uninstall.ps1
```

To restore the most recent Windows Terminal backup instead of editing keys in
place:

```powershell
pwsh -ExecutionPolicy Bypass -File .\uninstall.ps1 -RestoreLatestBackup
```

## Landing Page

Open `docs/index.html` locally or publish the `docs/` directory with GitHub
Pages.

## License

MIT. See [LICENSE](LICENSE).
