class Theme:
    def __init__(self):
        # Text
        self.text = ""
        self.subtext1 = ""
        self.subtext2 = ""

        # Bg
        self.base = ""
        self.mantle = ""
        self.surface1 = ""
        self.surface2 = ""
        self.overlay1 = ""
        self.overlay2 = ""

        # Misc
        self.accent = ""
        self.red = ""
        self.yellow = ""
        self.green = ""


def get_dark_theme() -> Theme:
    out = Theme()
    out.text = "#cdd6f4"
    out.subtext1 = "#bac2de"
    out.subtext2 = "#a6adc8"

    out.base = "#1e1e2e"
    out.mantle = "#181825"
    out.surface1 = "#45475a"
    out.surface2 = "#585b70"
    out.overlay1 = "#7f849c"
    out.overlay2 = "#9399b2"

    out.accent = "#89b4fa"
    out.red = "#f38ba8"
    out.yellow = "#f9e2af"
    out.green = "#a6e3a1"

    return out


def get_light_theme() -> Theme:
    out = Theme()
    out.text = "#4c4f69"
    out.subtext1 = "#5c5f77"
    out.subtext2 = "#6c6f85"

    out.base = "#eff1f5"
    out.mantle = "#e6e9ef"
    out.surface1 = "#ccd0da"
    out.surface2 = "#bcc0cc"
    out.overlay1 = "#9ca0b0"
    out.overlay2 = "#8c8fa1"

    out.accent = "#1e66f5"
    out.red = "#d20f39"
    out.yellow = "#df8e1d"
    out.green = "#40a02b"

    return out


current_theme: Theme = get_dark_theme()
