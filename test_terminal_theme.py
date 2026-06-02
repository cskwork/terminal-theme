import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


def load_module():
    spec = importlib.util.spec_from_file_location(
        "terminal_theme",
        Path(__file__).with_name("terminal-theme.py"),
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load terminal-theme.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def color_to_hex(color):
    return "#%02x%02x%02x" % tuple(
        round(color[key] * 255)
        for key in ("Red Component", "Green Component", "Blue Component")
    )


class TerminalThemeTest(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_iterm2_uses_oh_my_pi_titanium_terminal_defaults(self):
        profile = self.module.build_iterm2_profile(
            "test",
            "JetBrainsMonoNFM-Medium 15",
            None,
            0.92,
            2,
        )

        self.assertEqual("#e8ecf4", color_to_hex(profile["Foreground Color"]))
        self.assertEqual("#151820", color_to_hex(profile["Background Color"]))
        self.assertEqual("#00b4ff", color_to_hex(profile["Cursor Color"]))
        self.assertEqual("#0082b3", color_to_hex(profile["Selection Color"]))

    def test_windows_terminal_fragment_uses_theme_scheme(self):
        fragment = self.module.build_windows_terminal_fragment("Oh My Pi Titanium")
        scheme = fragment["schemes"][0]

        self.assertEqual("Oh My Pi Titanium", scheme["name"])
        self.assertEqual("#e8ecf4", scheme["foreground"])
        self.assertEqual("#151820", scheme["background"])
        self.assertEqual("#00b4ff", scheme["cursorColor"])
        self.assertEqual("Oh My Pi Titanium", fragment["profiles"]["defaults"]["colorScheme"])

    def test_wezterm_config_contains_palette_and_font(self):
        config = self.module.build_wezterm_config("Oh My Pi Titanium", "JetBrainsMono Nerd Font Mono", 15.0)

        self.assertIn('color_scheme = "Oh My Pi Titanium"', config)
        self.assertIn('foreground = "#e8ecf4"', config)
        self.assertIn('background = "#151820"', config)
        self.assertIn('font_size = 15.0', config)

    def test_orca_fragment_uses_terminal_color_overrides(self):
        fragment = self.module.build_orca_settings_fragment()
        overrides = fragment["settings"]["terminalColorOverrides"]

        self.assertEqual("#151820", overrides["background"])
        self.assertEqual("#e8ecf4", overrides["foreground"])
        self.assertEqual("#00b4ff", overrides["cursor"])
        self.assertEqual("#0082b3", overrides["selectionBackground"])
        self.assertEqual("#0f1216", overrides["cursorAccent"])
        self.assertEqual("#e8ecf4", overrides["brightWhite"])

    def test_all_target_writes_every_terminal_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = self.module.parse_args(["--target", "all", "--output-dir", tmp])
            outputs = self.module.write_targets(args)
            names = {path.name for path in outputs}

            self.assertEqual(
                {
                    "iterm2-dynamic-profile.json",
                    "wezterm.lua",
                    "windows-terminal.json",
                    "Microsoft.PowerShell_profile.ps1",
                    "orca-settings.json",
                },
                names,
            )
            windows = json.loads((Path(tmp) / "windows-terminal.json").read_text())
            self.assertEqual("Oh My Pi Titanium", windows["schemes"][0]["name"])
            orca = json.loads((Path(tmp) / "orca-settings.json").read_text())
            self.assertEqual("#151820", orca["settings"]["terminalColorOverrides"]["background"])

    def test_windows_live_installer_uses_titanium_palette(self):
        installer = Path(__file__).with_name("make-profile.ps1").read_text()
        uninstaller = Path(__file__).with_name("uninstall.ps1").read_text()

        for color in ("#151820", "#E8ECF4", "#00B4FF", "#0082B3"):
            self.assertIn(color, installer)
        self.assertNotIn("#1E1E2E", installer)
        self.assertIn("User.wezterm-port.", installer)
        self.assertIn("User.wezterm-port.", uninstaller)


if __name__ == "__main__":
    unittest.main()
