import os


class BaseConfig:
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    SECRET_KEY = os.getenv("SECRET_KEY")

    TINK_KEYSET_AEAD = os.getenv("TINK_KEYSET_AEAD")
    TINK_KEYSET_DAEAD = os.getenv("TINK_KEYSET_DAEAD")

    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY")

    FLASK_ADMINLTE_LAYOUT_OPTIONS = [
        # "control-sidebar-slide-open",
        "sidebar-mini",  # FLASK_ADMINLTE_SIDEBAR_MINI = True
        "layout-fixed",  # FLASK_ADMINLTE_SIDEBAR_FIXED = True
        "text-sm",  # FLASK_ADMINLTE_TEXT_SM = True
        # "sidebar-collapse",  # FLASK_ADMINLTE_SIDEBAR_COLLAPSE = True
        # "dark-mode",  # FLASK_ADMINLTE_DARK_MODE = True
        "layout-navbar-fixed",  # FLASK_ADMINLTE_NAVBAR_FIXED = True
        "layout-footer-fixed",  # FLASK_ADMINLTE_FOOTER_FIXED = True
        # "layout-top-nav",
    ]

    FLASK_ADMINLTE_NAVBAR_OPTIONS = [
        "main-header",
        "navbar",
        "navbar-expand",
        "navbar-dark",
        # "navbar-white",
        # "navbar-light",
    ]



class TestingConfig(DevelopmentConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
