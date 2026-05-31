# Plan

## Plain-Language Summary

`terminal-theme` will become the single repo for the Titanium terminal theme.
It will keep the Python generator, add the Windows live installer and
uninstaller from the old Windows-only repo, add a static landing page, then push
the new repo before retiring the old repo.

## Architecture

- Python generator stays dependency-free and writes portable config artifacts.
- Windows live setup stays in PowerShell because it must run on Windows and
  patch Windows Terminal plus PowerShell profile state.
- Landing page is static HTML/CSS in `docs/index.html` so GitHub Pages can serve
  it without a build step.
- Supergoal vault stays under `docs/changelog/2026-05-31-terminal-theme-consolidation/`.

## Contracts

- `terminal-theme.py --target all --output-dir <dir>` writes all generated
  portable artifacts.
- `make-profile.py` continues to behave as an iTerm2 compatibility entry point.
- `make-profile.ps1` patches Windows Terminal non-destructively and supports
  `-WhatIf`.
- `uninstall.ps1` removes only owned terminal-theme changes or restores the
  latest backup.
- `docs/index.html` must be readable as a static file and responsive.

## Design Read

Premium terminal-tool landing page: restrained dark Titanium palette, dense
but scannable product information, visible terminal preview in the first
viewport.

- `DESIGN_VARIANCE`: medium
- `MOTION_INTENSITY`: low
- `VISUAL_DENSITY`: medium-high

## Slices

| Slice | Files | Work | Acceptance Check |
| --- | --- | --- | --- |
| Windows migration | `make-profile.ps1`, `uninstall.ps1`, `README.md` | Port Windows live installer/uninstaller to Titanium and terminal-theme naming. | Static text checks, no old repo naming, PowerShell syntax if available. |
| Landing page | `docs/index.html`, `README.md` | Add dependency-free landing page and link it from docs. | Browser/static smoke check and content checks. |
| Verification docs | `docs/changelog/...` | Record claims, coverage, verification evidence. | Delivery evidence has GREEN verdict and coverage lines. |
| Delivery | GitHub remote | Commit/push new repo; retire old repo after evidence. | `gh repo view`, `git status`, and old repo archived/deleted evidence. |

## Human Feedback

### Plain-language brief

I will move the useful Windows-specific installer behavior into
`terminal-theme`, add a polished static landing page, commit and push the
unified repo, then retire the old Windows-only repo only after the replacement
is verified.

### Technical brief

The Python generator remains the cross-terminal artifact generator. The old
PowerShell installer will be migrated as Windows-only operational code because
it edits Windows Terminal `settings.json`, creates backups, optionally installs
oh-my-posh and JetBrainsMono Nerd Font, and manages a fenced `$PROFILE` block.
The landing page will be static HTML/CSS under `docs/index.html`. Tests will
cover generated config output, and verification will include smoke checks for
the docs and GitHub remote.

### Terms

- ANSI palette: the 16 terminal colors used by shell programs.
- Dynamic Profile: iTerm2 JSON profile loaded from its DynamicProfiles folder.
- `$PROFILE`: the PowerShell startup script for the current user.
- GitHub Pages: GitHub's static web hosting for files in a repo.

### Approval request

Approved for Build by the user's instruction: "yes do 1-4 the supergoal skill
use to make landing page for the repo".
