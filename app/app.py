from view.homepage import web_blueprint
from view.leitura_view import leitura_view
from view.login import login_blueprint
from view.recoverer_user_password import recoverer_user_password_blueprint
from view.register_user_view import register_user_blueprint
from view.gemini_view import gemini_bp
from view.minio_view import minio_view
from config import config
from datetime import timedelta
from ext import auth, database, language
from ext.data_encrypt import DataEncrypt
from ext.mail_sender import MailSender
from ext.token_generator import TokenGenerator
from flask import Flask, request, session  # type: ignore
from ext.admin.admin_lte import adminlte
from ext.admin.admin_main import admin

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.get("development"))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=120)

    language.init_app(app)
    database.init_app(app)
    MailSender.init_app(app)
    TokenGenerator.init_app(app)
    auth.init_app(app)
    DataEncrypt.init(app.secret_key)

    lang = language.lang

    @lang.localeselector
    def get_locale() -> str:
        override = request.args.get('lang')

        if override:
            session['lang'] = override

        return session.get('lang', 'pt')

    app.register_blueprint(web_blueprint)
    app.register_blueprint(leitura_view)
    app.register_blueprint(login_blueprint)
    app.register_blueprint(recoverer_user_password_blueprint)
    app.register_blueprint(register_user_blueprint)
    app.register_blueprint(gemini_bp)
    app.register_blueprint(minio_view)
    adminlte.init_app(app)
    admin.init_app(app)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0", port=5006)
