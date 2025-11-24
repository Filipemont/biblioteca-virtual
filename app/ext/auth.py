from flask import redirect, url_for  # type: ignore
from flask_login import LoginManager  # type: ignore


login = LoginManager()


def init_app(app):
    login.init_app(app)
    login.login_view = "login"
    login.login_message = "Faça o Login para acessar essa página"


@login.unauthorized_handler
def unauthorized() -> redirect:
    return redirect(url_for('login_blueprint.login'))
