from flask_sqlalchemy import SQLAlchemy  # type: ignore


db: object = SQLAlchemy()


def init_app(app) -> None:
    db.init_app(app)
