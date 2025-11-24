from flask import Flask  # type: ignore
from flask_babelex import Babel  # type: ignore


lang: object = Babel()


def init_app(app: Flask) -> None:
    lang.init_app(app)
