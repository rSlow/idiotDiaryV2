from config.settings import BASE_DIR

DATA_DIR = BASE_DIR / "apps" / "free_shaurma" / "data"

RESOURCES_DIR = DATA_DIR / "resources"
TEMPLATES_DIR = DATA_DIR / "templates"
FONTS_DIR = RESOURCES_DIR / "fonts"

font_android = (FONTS_DIR / "Roboto-Medium.ttf").as_posix()
font_iphone_bold = (FONTS_DIR / "sfuidisplay_bold.ttf").as_posix()
font_iphone_thin = (FONTS_DIR / "sfuidisplay_thin.ttf").as_posix()

template_sberbank_android = TEMPLATES_DIR / "android" / "sberbank" / "sberbank.png"
template_sberbank_iphone = TEMPLATES_DIR / "iphone" / "sberbank" / "sberbank.png"

template_tinkoff_phone_android = TEMPLATES_DIR / "android" / "tinkoff" / "tinkoff_phone.png"
template_tinkoff_phone_iphone = TEMPLATES_DIR / "iphone" / "tinkoff" / "tinkoff_phone.png"

tinkoff_arrow = RESOURCES_DIR / "layouts" / "arrow.png"
