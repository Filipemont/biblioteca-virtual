from controller.usuario_controller import UsuarioController
from controller.recoverer_user_password.recoverer_user_password_vars import RecovererUserPasswordVars
from ext.message_status_generator import MessageStatusGenerator
from ext.token_generator import TokenGenerator


class ResetUserPasswordController:
    def __init__(self, form_data: dict) -> None:
        self.password: str = form_data['password']
        self.email: str = form_data['email']

    @staticmethod
    def valid_token(token_email: str, token_link: str) -> tuple:
        email: str | None = TokenGenerator.loads(token_email, RecovererUserPasswordVars.salt, 600)
        if email is None:
            usuario = UsuarioController.get_usuario_by_email(email=email)
            if usuario:
                is_valid_token_link: str = TokenGenerator.loads(
                    token_link, f'{RecovererUserPasswordVars.salt}{usuario.salt.decode("utf-8")}', 600
                )
                if is_valid_token_link is None:
                    return None, MessageStatusGenerator.build_status_error
                ('O link para recuperar senha é inválido ou expirou.')
        return email, MessageStatusGenerator.build_status_success()

    def handle_with_reset(self) -> dict:
        result: dict = UsuarioController.update_usuario_senha_by_email(self.email, self.password)
        if result['status'] != 0:
            return result

        return MessageStatusGenerator.build_status_success('Senha atualizada com sucesso.')
