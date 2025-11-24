from controller.usuario_controller import UsuarioController
from controller.login.login_user_vars import LoginUserVars
from controller.register_user.register_user_vars import RegisterUserVars
from ext.auth import login
from ext.hash_generator import HashGenerator
from ext.mail_sender import MailSender
from ext.message_status_generator import MessageStatusGenerator
from ext.token_generator import TokenGenerator
from flask import url_for  # type: ignore
from model.usuario_model import UsuarioModel
from werkzeug.urls import url_parse  # type: ignore


class LoginController:
    def __init__(self, login: str, senha: str) -> None:
        self.usuario: object = UsuarioController.get_usuario_by_email(login)
        self.senha: str = senha
        self.status_error: dict = None
        self.token_get: str = ''
        self.token_post: str = ''
        self.token_parameter: str = ''
        self.result: dict = {}

    def _set_token_id(self) -> None:
        salt_get: str = LoginUserVars.salt_get + self.usuario.salt.decode('utf-8')
        salt_post: str = LoginUserVars.salt_post + self.usuario.salt.decode('utf-8')
        self.token_get = TokenGenerator.get_token(self.usuario.id, salt_get)
        self.token_post = TokenGenerator.get_token(self.usuario.id, salt_post)
        self.token_parameter = TokenGenerator.get_token(self.usuario.id, LoginUserVars.salt_parameter)

    def __check_activated(self) -> None:
        if self.usuario.status == 1:
            return True
        token_link: str = TokenGenerator.get_token(
            self.usuario.get_email(), f"{RegisterUserVars.salt}{self.usuario.salt.decode('utf8')}"
        )
        token_email: str = TokenGenerator.get_token(self.usuario.get_email(), RegisterUserVars.salt)
        MailSender.send_confirmation_email(self.usuario.get_email(), token_link, token_email)
        self.result = MessageStatusGenerator.build_status_error('Usuário não ativado, verifique seu email para ativar!')
        return False

    def check_usr(self, password: str) -> bool | None:
        if self.usuario:
            if not self.__check_activated():
                return False

            if self.usuario.senha == HashGenerator.get_hashed_password(password, self.usuario.salt):
                return True
            else:
                self.result = MessageStatusGenerator.build_status_error('Senha Inválida.')
        else:
            self.result = MessageStatusGenerator.build_status_error('Email não cadastrado')

        return None

    def check_page(self, next_page: str) -> str:
        if not next_page or url_parse(next_page).netloc != "":
            return url_for("login_blueprint.login")
        return next_page

    def get_user_name(self) -> str:
        return self.usuario.get_nome()

    @staticmethod
    @login.user_loader
    def load_user(usuario_codigo: str) -> UsuarioModel:
        return UsuarioController.get_usuario_by_codigo(usuario_codigo)
