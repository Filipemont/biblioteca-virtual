from controller.usuario_controller import UsuarioController
from controller.recoverer_user_password.recoverer_user_password_vars import RecovererUserPasswordVars
from ext.mail_sender import MailSender
from ext.message_status_generator import MessageStatusGenerator
from ext.token_generator import TokenGenerator


class RecovererUserPasswordController:
    def __init__(self, form_data: dict) -> None:
        self.email: str = form_data['email']

    def handle_recoverer_password(self) -> dict:
        if UsuarioController.check_email_exist(self.email) is False:
            return MessageStatusGenerator.build_status_error('Erro: o email não existe em nossa base de dados.')

        usuario = UsuarioController.get_usuario_by_email(self.email)

        token_email: str = TokenGenerator.get_token(self.email, RecovererUserPasswordVars.salt)
        token_link: str = TokenGenerator.get_token(
            self.email, f"{RecovererUserPasswordVars.salt}{usuario.salt.decode('utf8')}"
        )

        result: dict = MailSender.send_recoverer_password_email(self.email, token_link, token_email)

        if result['status'] != 0:
            return result

        return MessageStatusGenerator.build_status_success(
            'Um link de para recuperar senha foi enviado para seu email.'
        )
