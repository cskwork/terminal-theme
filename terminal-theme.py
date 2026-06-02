#!/usr/bin/env python3
"""Generate Oh My Pi Titanium theme files for terminal applications.

Targets:
    iterm2            iTerm2 Dynamic Profile JSON
    wezterm           WezTerm Lua config snippet
    windows-terminal  Windows Terminal settings fragment
    powershell        PowerShell profile styling snippet
    orca              Orca terminalColorOverrides JSON
    all               all portable target files in one output directory

Usage:
    python3 terminal-theme.py --set-default
    python3 terminal-theme.py --target all --output-dir dist
    python3 terminal-theme.py --target wezterm --output wezterm.lua
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import uuid
from pathlib import Path

THEME_NAME = "Oh My Pi Titanium"
ITERM_PROFILE_NAME = "Terminal Theme (Oh My Pi Titanium)"
ITERM_FONT = "JetBrainsMonoNFM-Medium 15"
WEZTERM_FONT = "JetBrainsMono Nerd Font Mono"
OUTPUT_BASENAME = "terminal-theme"
TARGETS = ("iterm2", "wezterm", "windows-terminal", "powershell", "orca")

OMP_TITANIUM = {
    "base": "#151820",
    "crust": "#0f1216",
    "surface2": "#2a3038",
    "surface1": "#1f252d",
    "text": "#e8ecf4",
    "muted": "#9ca3b0",
    "dim": "#6b7280",
    "red": "#ff4757",
    "green": "#00ff88",
    "yellow": "#ffb347",
    "gold": "#d4c090",
    "blue": "#00b4ff",
    "deep_blue": "#0082b3",
}

ANSI_KEYS = ("crust", "red", "green", "yellow", "deep_blue", "gold", "blue", "muted")
BRIGHT_KEYS = ("surface2", "red", "green", "gold", "blue", "gold", "blue", "text")


def hex_to_color(hex_str: str) -> dict:
    h = hex_str.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4))
    return {
        "Red Component": r,
        "Green Component": g,
        "Blue Component": b,
        "Alpha Component": 1.0,
        "Color Space": "sRGB",
    }


def rgb_tuple(hex_str: str) -> tuple[int, int, int]:
    h = hex_str.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def ansi_palette() -> tuple[list[str], list[str]]:
    p = OMP_TITANIUM
    return [p[key] for key in ANSI_KEYS], [p[key] for key in BRIGHT_KEYS]


def base_iterm2_profile(name: str, font: str) -> dict:
    return {
        "Name": name,
        "Guid": str(uuid.uuid4()),
        "Normal Font": font,
        "Non Ascii Font": font,
        "Use Non-ASCII Font": False,
        "ASCII Anti Aliased": True,
        "Non-ASCII Anti Aliased": True,
        "Horizontal Spacing": 1.0,
        "Vertical Spacing": 1.05,
        "Cursor Type": 2,
        "Blinking Cursor": True,
        "Transparency": 0.0,
        "Initial Use Transparency": False,
        "Use Bold Font": True,
        "Use Bright Bold": True,
        "Use Italic Font": True,
        "Sync Title": True,
        "Silence Bell": True,
        "Visual Bell": True,
        "Flashing Bell": False,
        "Scrollback Lines": 10000,
        "Unlimited Scrollback": False,
        "Custom Command": "No",
        "Working Directory": str(Path.home()),
        "Custom Directory": "Recycle",
    }


def build_iterm2_profile(
    name: str,
    font: str,
    backdrop: str | None,
    blend: float,
    bg_mode: int,
) -> dict:
    p = OMP_TITANIUM
    ansi, bright = ansi_palette()
    profile = base_iterm2_profile(name, font)
    profile.update(
        {
            "Background Color": hex_to_color(p["base"]),
            "Foreground Color": hex_to_color(p["text"]),
            "Bold Color": hex_to_color(p["text"]),
            "Link Color": hex_to_color(p["blue"]),
            "Cursor Color": hex_to_color(p["blue"]),
            "Cursor Text Color": hex_to_color(p["crust"]),
            "Cursor Guide Color": hex_to_color(p["surface1"]),
            "Selection Color": hex_to_color(p["deep_blue"]),
            "Selected Text Color": hex_to_color(p["text"]),
            "Badge Color": hex_to_color(p["red"]),
            "Tab Color": hex_to_color(p["base"]),
            "Underline Color": hex_to_color(p["blue"]),
        }
    )
    for index, value in enumerate(ansi + bright):
        profile[f"Ansi {index} Color"] = hex_to_color(value)
    if backdrop:
        profile["Background Image Location"] = str(Path(backdrop).expanduser().resolve())
        profile["Background Image Mode"] = bg_mode
        profile["Blend"] = blend
        profile["Blur"] = False
    return profile


build_profile = build_iterm2_profile


def build_wezterm_config(name: str, font_family: str, font_size: float) -> str:
    p = OMP_TITANIUM
    ansi, bright = ansi_palette()
    lua_ansi = ", ".join(json.dumps(color) for color in ansi)
    lua_brights = ", ".join(json.dumps(color) for color in bright)
    return f"""local wezterm = require "wezterm"

return {{
  color_schemes = {{
    [{json.dumps(name)}] = {{
      foreground = {json.dumps(p["text"])},
      background = {json.dumps(p["base"])},
      cursor_bg = {json.dumps(p["blue"])},
      cursor_fg = {json.dumps(p["crust"])},
      cursor_border = {json.dumps(p["blue"])},
      selection_fg = {json.dumps(p["text"])},
      selection_bg = {json.dumps(p["deep_blue"])},
      ansi = {{ {lua_ansi} }},
      brights = {{ {lua_brights} }},
    }},
  }},
  color_scheme = {json.dumps(name)},
  font = wezterm.font({json.dumps(font_family)}, {{ weight = "Medium" }}),
  font_size = {font_size:.1f},
  default_cursor_style = "BlinkingBlock",
}}
"""


def build_windows_terminal_fragment(name: str) -> dict:
    p = OMP_TITANIUM
    ansi, bright = ansi_palette()
    scheme_keys = ("black", "red", "green", "yellow", "blue", "purple", "cyan", "white")
    bright_keys = tuple(f"bright{key[:1].upper()}{key[1:]}" for key in scheme_keys)
    colors = dict(zip(scheme_keys, ansi)) | dict(zip(bright_keys, bright))
    scheme = {
        "name": name,
        "foreground": p["text"],
        "background": p["base"],
        "cursorColor": p["blue"],
        "selectionBackground": p["deep_blue"],
        **colors,
    }
    return {"schemes": [scheme], "profiles": {"defaults": {"colorScheme": name}}}


def build_orca_settings_fragment() -> dict:
    p = OMP_TITANIUM
    ansi, bright = ansi_palette()
    return {
        "settings": {
            "terminalColorOverrides": {
                "background": p["base"],
                "foreground": p["text"],
                "cursor": p["blue"],
                "selectionBackground": p["deep_blue"],
                "selectionForeground": p["text"],
                "cursorAccent": p["crust"],
                "bold": p["text"],
                "black": ansi[0],
                "red": ansi[1],
                "green": ansi[2],
                "yellow": ansi[3],
                "blue": ansi[4],
                "magenta": ansi[5],
                "cyan": ansi[6],
                "white": ansi[7],
                "brightBlack": bright[0],
                "brightRed": bright[1],
                "brightGreen": bright[2],
                "brightYellow": bright[3],
                "brightBlue": bright[4],
                "brightMagenta": bright[5],
                "brightCyan": bright[6],
                "brightWhite": bright[7],
            }
        }
    }


def psstyle_color(hex_str: str) -> str:
    r, g, b = rgb_tuple(hex_str)
    return f'"$esc[38;2;{r};{g};{b}m"'


def build_powershell_profile(name: str) -> str:
    p = OMP_TITANIUM
    return f"""# Generated by terminal-theme: {name}
# Full terminal palette colors belong in iTerm2, WezTerm, Windows Terminal, or Orca.
$esc = [char]27

if (Get-Variable PSStyle -ErrorAction SilentlyContinue) {{
  $PSStyle.Formatting.Error = {psstyle_color(p["red"])}
  $PSStyle.Formatting.Warning = {psstyle_color(p["yellow"])}
  $PSStyle.Formatting.Verbose = {psstyle_color(p["muted"])}
  $PSStyle.Formatting.Debug = {psstyle_color(p["blue"])}
  $PSStyle.Formatting.TableHeader = {psstyle_color(p["gold"])}
}}

if ($Host.PrivateData) {{
  $Host.PrivateData.ErrorForegroundColor = "Red"
  $Host.PrivateData.WarningForegroundColor = "Yellow"
  $Host.PrivateData.DebugForegroundColor = "Cyan"
  $Host.PrivateData.VerboseForegroundColor = "Gray"
  $Host.PrivateData.ProgressForegroundColor = "Cyan"
  $Host.PrivateData.ProgressBackgroundColor = "Black"
}}
"""


def write_text(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def write_json(path: Path, content: dict) -> Path:
    return write_text(path, json.dumps(content, indent=2) + "\n")


def write_profile(profile: dict, output: Path | None) -> Path:
    return write_json(output or default_iterm2_output(), {"Profiles": [profile]})


def default_iterm2_output() -> Path:
    return Path.home() / f"Library/Application Support/iTerm2/DynamicProfiles/{OUTPUT_BASENAME}.json"


def set_iterm2_default(guid: str) -> None:
    subprocess.run(
        ["defaults", "write", "com.googlecode.iterm2", "Default Bookmark Guid", "-string", guid],
        check=True,
    )


set_default = set_iterm2_default


def write_iterm2(args: argparse.Namespace, output: Path | None) -> Path:
    profile = build_iterm2_profile(args.name, args.font, args.backdrop, args.blend, args.bg_mode)
    out = write_profile(profile, output)
    print(f"Wrote {out}")
    print(f"iTerm2 profile: {profile['Name']!r}  (GUID {profile['Guid']})")
    if args.set_default:
        set_iterm2_default(profile["Guid"])
        print("Set as iTerm2 default profile.")
    return out


def write_portable_target(target: str, args: argparse.Namespace, output: Path) -> Path:
    if target == "wezterm":
        return write_text(output, build_wezterm_config(args.theme_name, args.wezterm_font, args.wezterm_font_size))
    if target == "windows-terminal":
        return write_json(output, build_windows_terminal_fragment(args.theme_name))
    if target == "powershell":
        return write_text(output, build_powershell_profile(args.theme_name))
    if target == "orca":
        return write_json(output, build_orca_settings_fragment())
    raise ValueError(f"Unsupported portable target: {target}")


def target_output_path(output_dir: Path, target: str) -> Path:
    names = {
        "iterm2": "iterm2-dynamic-profile.json",
        "wezterm": "wezterm.lua",
        "windows-terminal": "windows-terminal.json",
        "powershell": "Microsoft.PowerShell_profile.ps1",
        "orca": "orca-settings.json",
    }
    return output_dir / names[target]


def write_targets(args: argparse.Namespace) -> list[Path]:
    if args.target == "iterm2":
        return [write_iterm2(args, args.output)]
    if args.output and args.target == "all":
        raise SystemExit("--output can only be used with a single target")
    if args.set_default:
        raise SystemExit("--set-default only applies to --target iterm2")

    targets = TARGETS if args.target == "all" else (args.target,)
    outputs = []
    for target in targets:
        path = args.output or target_output_path(args.output_dir, target)
        if target == "iterm2":
            outputs.append(write_iterm2(args, path))
        else:
            out = write_portable_target(target, args, path)
            print(f"Wrote {out}")
            outputs.append(out)
    return outputs


def parse_args(argv: list[str]) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", choices=(*TARGETS, "all"), default="iterm2")
    ap.add_argument("--theme-name", default=THEME_NAME, help="Theme name used in portable configs.")
    ap.add_argument("--name", default=ITERM_PROFILE_NAME, help="Profile name shown in iTerm2.")
    ap.add_argument("--font", default=ITERM_FONT, help='iTerm2 font string: "PostScriptName Size".')
    ap.add_argument("--wezterm-font", default=WEZTERM_FONT, help="WezTerm font family.")
    ap.add_argument("--wezterm-font-size", type=float, default=15.0, help="WezTerm font size.")
    ap.add_argument("--backdrop", default=None, help="Optional iTerm2 background image path.")
    ap.add_argument("--blend", type=float, default=0.92, help="iTerm2 background image blend.")
    ap.add_argument("--bg-mode", type=int, default=2, choices=[0, 1, 2, 3], help="iTerm2 image mode.")
    ap.add_argument("--output", type=Path, default=None, help="Output path for a single target.")
    ap.add_argument("--output-dir", type=Path, default=Path("dist"), help="Output directory for --target all.")
    ap.add_argument("--set-default", action="store_true", help="Set generated iTerm2 profile as default.")
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    write_targets(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
