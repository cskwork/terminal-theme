# Terminal Theme Consolidation

Mode: LEGACY with UI/UX overlay.

Objective: consolidate `cskwork/windows-terminal-wezterm-port` into
`cskwork/terminal-theme`, commit and push the unified repo, retire the old
Windows-only repo after migration evidence exists, and add a landing page for
the unified project.

## Priority Rules

- Keep terminal palette values single-source so iTerm2, WezTerm, Windows
  Terminal, and PowerShell-adjacent output stay consistent.
- Preserve non-destructive Windows behavior: backup before modifying settings,
  fenced PowerShell profile edits, and an uninstall path.
- Do not delete or archive the old repo until the new repo has the migrated
  behavior committed and pushed.
- Avoid promising PowerShell terminal palette control; PowerShell can style
  shell output, while the terminal app owns the ANSI palette.
- Keep generated artifacts easy to copy into each terminal's native config.
- Landing page must show the actual product quickly: supported terminals,
  Titanium colors, commands, and generated outputs.
- Favor static, dependency-free files so the repo remains portable.
- Verification must include Python tests, syntax checks, generated artifact
  smoke checks, and GitHub remote state.

## Codebase Map

- `terminal-theme.py`: main Python generator for iTerm2, WezTerm, Windows
  Terminal JSON fragments, and PowerShell profile snippets.
- `make-profile.py`: compatibility wrapper for the old iTerm2 command.
- `test_terminal_theme.py`: Python unit tests for generated colors and output
  files.
- `README.md`: user-facing install and target docs.
- `make-profile.ps1` and `uninstall.ps1`: Windows Terminal live installer and
  rollback path migrated from `windows-terminal-wezterm-port`.
- `docs/index.html`: static landing page for GitHub Pages.

## Decisions

- Decision: migrate the Windows installer instead of treating generated
  fragments as enough.
- Reason: the old repo contains unique live-patching, backup, font install,
  oh-my-posh, and uninstall behavior that generated fragments do not replace.
- Decision: use Oh My Pi Titanium as the unified palette, not Catppuccin Mocha.
- Reason: the current repo objective is a terminal-wide Oh My Pi Titanium theme.
- Decision: keep `make-profile.py` as a compatibility wrapper.
- Reason: existing iTerm2 users can keep old commands while new docs use
  `terminal-theme.py`.
- Decision: add `docs/index.html` as the landing page.
- Reason: GitHub Pages can serve `/docs` without a build system.

## Human Approval

The user wrote: "yes do 1-4 the supergoal skill use to make landing page for
the repo". This records approval to Build for the plan in `plan.md`.
