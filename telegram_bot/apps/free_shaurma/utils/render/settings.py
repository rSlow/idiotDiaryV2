from config.settings import BASE_DIR

DATA_DIR = BASE_DIR / "apps" / "free_shaurma" / "data"

font_android = str(DATA_DIR / "resources" / "fonts" / "Roboto-Medium.ttf")
font_iphone_bold = str(DATA_DIR / "resources" / "fonts" / "sfuidisplay_bold.ttf")
font_iphone_thin = str(DATA_DIR / "resources" / "fonts" / "sfuidisplay_thin.ttf")

template_sberbank_android = DATA_DIR / "templates" / "android" / "sberbank" / "sberbank.png"
template_sberbank_iphone = DATA_DIR / "templates" / "iphone" / "sberbank" / "sberbank.png"

template_tinkoff_phone_android = DATA_DIR / "templates" / "android" / "tinkoff" / "tinkoff_phone.png"
template_tinkoff_phone_iphone = DATA_DIR / "templates" / "iphone" / "tinkoff" / "tinkoff_phone.png"

tinkoff_arrow = DATA_DIR / "resources" / "layouts" / "arrow.png"
