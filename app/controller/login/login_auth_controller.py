import pyotp  # type: ignore
import time
from controller.autenticacao_controller import AutenticacaoController
from controller.usuario_controller import UsuarioController
from controller.login.login_user_vars import LoginUserVars
from ext.mail_sender import MailSender
from ext.message_status_generator import MessageStatusGenerator
from ext.token_generator import TokenGenerator
from model.usuario_model import UsuarioModel


class LoginAuthController:
    def __init__(self) -> None:
        self.secret: str = ''
        self.__time_token: int = None
        self.token: str = ''
        self.salt_value: str = ''
        self.result: dict = {}
        self.id: str | None = None
        self.usuario: object = None
        pass

    def _load_user(self) -> None:
        usuario: object = UsuarioController.get_usuario_by_codigo(self.usuario.id)
        return usuario

    def get_totp(self, secret: str) -> object:
        return pyotp.TOTP(secret)

    def send_mail_auth(self) -> None:
        self.secret = pyotp.random_base32()
        totp: object = self.get_totp(self.secret)
        self.__time_token = int(time.time())
        self.token = totp.at(self.__time_token)
        AutenticacaoController.set_autenticacao(self.__time_token, self.usuario.id, self.secret)
        MailSender.send_confirmation_login(self.usuario.get_email(), self.usuario.get_nome(), self.token)

    def validate_token(self, token: str) -> bool:
        autenticacao: object = AutenticacaoController.get_autenticacao_by_codigo_usuario(self.usuario.id)
        totp: object = self.get_totp(autenticacao.secret)
        if not totp.verify(token, for_time=autenticacao.horario_chave, valid_window=1):
            self.result = MessageStatusGenerator.build_status_error(
                'Erro: Código de autenticação incorreto, faça login novamente.'
            )
            return False
        return True

    def __set_salt_value_from_token(self, parameter_token: str, method: str) -> None:
        user_id: str = TokenGenerator.loads(parameter_token, LoginUserVars.salt_parameter, 3600)
        usuario: object = UsuarioController.get_usuario_by_codigo(user_id)
        self.salt_value = getattr(LoginUserVars, f'salt_{method.lower()}') + usuario.salt.decode('utf-8')

    def handle_autentication(self, token: str, expiration_time: float, method: str, parameter_token) -> dict:
        self.__set_salt_value_from_token(parameter_token, method)
        self.id = TokenGenerator.loads(token, self.salt_value, expiration_time)
        if self.id:
            self.usuario = UsuarioModel.query.filter_by(id=self.id).first()
            self.result = MessageStatusGenerator.build_status_success()
        else:
            self.result = MessageStatusGenerator.build_status_error(
                'Erro: A página de autenticação expirou, faça login novamente.'
            )
