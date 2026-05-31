# Changelog 2026-05-31

## terminal-theme consolidation

- Decision: consolidate the Windows Terminal repo into `terminal-theme` before
  retiring the old repository.
- Reason: `windows-terminal-wezterm-port` includes live Windows installer,
  backup, oh-my-posh, font install, profile wiring, and uninstall behavior not
  covered by generated fragments alone.
- Decision: add a static landing page under `docs/index.html`.
- Reason: the repo needs a first-class product surface without adding a build
  system.
