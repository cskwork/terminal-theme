#!/usr/bin/env python3
"""Generate an iTerm2 Dynamic Profile that ports WezTerm aesthetics to iTerm2.

Ports: Catppuccin Mocha palette, configurable Nerd Font, optional darkened
background image, blinking-block cursor, generous line spacing. Writes the
profile to iTerm2's DynamicProfiles directory (auto-loaded, no restart).

Usage:
    python3 make-profile.py                          # defaults, no background image
    python3 make-profile.py --backdrop path/img.jpg  # with a background image
    python3 make-profile.py --backdrop img --blend 0.92  # near-solid background
    python3 make-profile.py --set-default            # also mark as iTerm2 default
"""
import argparse
import json
import sys
import uuid
from pathlib import Path

CATPPUCCIN_MOCHA = {
    "base": "#1e1e2e",
    "text": "#cdd6f4",
    "rosewater": "#f5e0dc",
    "crust": "#11111b",
    "surface2": "#585b70",
    "surface1": "#45475a",
    "surface0": "#313244",
    "subtext0": "#a6adc8",
    "subtext1": "#bac2de",
    "red": "#f38ba8",
    "green": "#a6e3a1",
    "yellow": "#f9e2af",
    "blue": "#89b4fa",
    "pink": "#f5c2e7",
    "teal": "#94e2d5",
    "peach": "#fab387",
    "mauve": "#cba6f7",
    "lavender": "#b4befe",
}


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


def build_profile(
    name: str,
    font: str,
    backdrop: str | None,
    blend: float,
    bg_mode: int,
) -> dict:
    p = CATPPUCCIN_MOCHA
    profile = {
        "Name": name,
        "Guid": str(uuid.uuid4()),
        "Normal Font": font,
        "Non Ascii Font": font,
        "Use Non-ASCII Font": False,
        "ASCII Anti Aliased": True,
        "Non-ASCII Anti Aliased": True,
        "Horizontal Spacing": 1.0,
        "Vertical Spacing": 1.05,
        "Background Color": hex_to_color(p["base"]),
        "Foreground Color": hex_to_color(p["text"]),
        "Bold Color": hex_to_color(p["text"]),
        "Link Color": hex_to_color(p["blue"]),
        "Cursor Color": hex_to_color(p["rosewater"]),
        "Cursor Text Color": hex_to_color(p["crust"]),
        "Cursor Guide Color": hex_to_color(p["surface1"]),
        "Selection Color": hex_to_color(p["surface2"]),
        "Selected Text Color": hex_to_color(p["text"]),
        "Badge Color": hex_to_color(p["red"]),
        "Tab Color": hex_to_color(p["base"]),
        "Underline Color": hex_to_color(p["rosewater"]),
        "Ansi 0 Color": hex_to_color(p["surface1"]),
        "Ansi 1 Color": hex_to_color(p["red"]),
        "Ansi 2 Color": hex_to_color(p["green"]),
        "Ansi 3 Color": hex_to_color(p["yellow"]),
        "Ansi 4 Color": hex_to_color(p["blue"]),
        "Ansi 5 Color": hex_to_color(p["pink"]),
        "Ansi 6 Color": hex_to_color(p["teal"]),
        "Ansi 7 Color": hex_to_color(p["subtext1"]),
        "Ansi 8 Color": hex_to_color(p["surface2"]),
        "Ansi 9 Color": hex_to_color(p["red"]),
        "Ansi 10 Color": hex_to_color(p["green"]),
        "Ansi 11 Color": hex_to_color(p["yellow"]),
        "Ansi 12 Color": hex_to_color(p["blue"]),
        "Ansi 13 Color": hex_to_color(p["pink"]),
        "Ansi 14 Color": hex_to_color(p["teal"]),
        "Ansi 15 Color": hex_to_color(p["subtext0"]),
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
    if backdrop:
        profile["Background Image Location"] = str(Path(backdrop).expanduser().resolve())
        profile["Background Image Mode"] = bg_mode
        profile["Blend"] = blend
        profile["Blur"] = False
    return profile


def write_profile(profile: dict, output: Path | None) -> Path:
    if output is None:
        output = (
            Path.home()
            / "Library/Application Support/iTerm2/DynamicProfiles/wezterm-port.json"
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"Profiles": [profile]}, indent=2))
    return output


def set_default(guid: str) -> None:
    import subprocess
    subprocess.run(
        ["defaults", "write", "com.googlecode.iterm2", "Default Bookmark Guid",
         "-string", guid],
        check=True,
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", default="WezTerm Port (Catppuccin Mocha)",
                    help="Profile name shown in iTerm2.")
    ap.add_argument("--font", default="JetBrainsMonoNFM-Medium 15",
                    help='iTerm2 font string: "PostScriptName Size". '
                         'Default: JetBrainsMono Nerd Font Mono Medium 15.')
    ap.add_argument("--backdrop", default=None,
                    help="Path to a background image. Omit for a solid background.")
    ap.add_argument("--blend", type=float, default=0.92,
                    help="0=image only, 1=background color only. Default 0.92 "
                         "(strongly darkened — readable over any image).")
    ap.add_argument("--bg-mode", type=int, default=2, choices=[0, 1, 2, 3],
                    help="0=Stretch, 1=Tile, 2=Fill (default), 3=Fit.")
    ap.add_argument("--output", type=Path, default=None,
                    help="JSON output path. Default: iTerm2 DynamicProfiles dir.")
    ap.add_argument("--set-default", action="store_true",
                    help="Set as iTerm2 default profile after writing.")
    args = ap.parse_args()

    profile = build_profile(args.name, args.font, args.backdrop, args.blend, args.bg_mode)
    out = write_profile(profile, args.output)
    print(f"Wrote {out}")
    print(f"Profile: {profile['Name']!r}  (GUID {profile['Guid']})")
    if args.backdrop:
        print(f"Backdrop: {profile['Background Image Location']}  (blend {args.blend})")
    else:
        print("Backdrop: none (solid Catppuccin Mocha base)")

    if args.set_default:
        set_default(profile["Guid"])
        print("Set as iTerm2 default profile.")
    else:
        print("Tip: pass --set-default to make this the default for new windows.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
