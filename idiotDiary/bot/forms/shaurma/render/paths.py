from pathlib import Path

SRC_DIR = Path(__file__).parent / "src"

LAYOUTS_DIR = SRC_DIR / "layouts"
TEMPLATES_DIR = SRC_DIR / "templates"
FONTS_DIR = SRC_DIR / "fonts"

font_android = (FONTS_DIR / "Roboto-Medium.ttf").as_posix()
font_iphone_bold = (FONTS_DIR / "sfuidisplay_bold.ttf").as_posix()
font_iphone_thin = (FONTS_DIR / "sfuidisplay_thin.ttf").as_posix()
font_iphone_medium = (FONTS_DIR / "sfuidisplay_medium.otf").as_posix()
