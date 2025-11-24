from controller.usuario_controller import UsuarioController
from controller.register_user.register_user_vars import RegisterUserVars
from ext.database import db
from ext.message_status_generator import MessageStatusGenerator
from ext.token_generator import TokenGenerator


class ConfirmEmailController:
    @staticmethod
    def __get_email_by_token(token: str) -> str:
        return TokenGenerator.loads(token, RegisterUserVars.salt, 3600)

    @staticmethod
    def __valid_usuario(email: str, token_link: str) -> dict:
        usuario: object = UsuarioController.get_usuario_by_email(email)
        if usuario:
            is_valid_token_link: str | None = TokenGenerator.loads(
                token_link, f'{RegisterUserVars.salt}{usuario.salt.decode("utf-8")}', 3600
            )
            if is_valid_token_link is not None:
                if usuario.status == 1:
                    return MessageStatusGenerator.build_status_success(f'Email já foi validado! {usuario.get_email()}')

                usuario.status = 1
                db.session.commit()
                return MessageStatusGenerator.build_status_success(
                    f'Email confirmado com sucesso! {usuario.get_email()}'
                )
        return MessageStatusGenerator.build_status_error('O link de ativação é inválido ou expirou.')

    @staticmethod
    def valid_token(token_email: str, token_link: str) -> dict:
        email: str | None = ConfirmEmailController.__get_email_by_token(token_email)
        if email is not None:
            return ConfirmEmailController.__valid_usuario(email, token_link)
        return MessageStatusGenerator.build_status_error('O link de ativação é inválido ou expirou.')
