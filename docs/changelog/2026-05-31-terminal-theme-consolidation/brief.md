# Brief

## Goal

Make `terminal-theme` the unified home for Oh My Pi Titanium terminal theming,
covering iTerm2, WezTerm, Windows Terminal, and PowerShell-adjacent styling.

## Acceptance Criteria

- `terminal-theme` changes are committed and pushed to
  `https://github.com/cskwork/terminal-theme`.
- Windows Terminal installer behavior from `windows-terminal-wezterm-port` is
  migrated into `terminal-theme`, including non-destructive backups, settings
  patching, optional oh-my-posh/font install, fenced PowerShell profile wiring,
  and uninstall support.
- `README.md` documents the unified repo, generated fragments, Windows live
  installer, uninstall path, and landing page.
- A static landing page exists for the repo and presents the supported
  terminals, Titanium palette, commands, and project value.
- Verification covers Python generator tests, script syntax where available,
  generated artifact smoke checks, landing page smoke checks, and GitHub remote
  state.
- The old `cskwork/windows-terminal-wezterm-port` repo is retired only after the
  new repo is pushed and verified.

## Non-Goals

- Building a packaged native installer for every terminal.
- Modifying a live Windows machine from macOS.
- Guaranteeing PowerShell controls terminal palette values; it can style
  PowerShell output while the terminal app owns the palette.

## Validation

The old Windows repo contains unique behavior not present in the initial
`terminal-theme` generator: Windows Terminal `settings.json` mutation,
timestamped backups, oh-my-posh/font installation, fenced `$PROFILE` wiring,
and uninstall support. These are required before retiring the old repo.

Decision: GO
