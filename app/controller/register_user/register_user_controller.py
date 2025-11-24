from controller.usuario_controller import UsuarioController
from controller.usuario_papel_controller import UsuarioPapelController
from controller.register_user.register_user_vars import RegisterUserVars
from ext.mail_sender import MailSender
from ext.message_status_generator import MessageStatusGenerator
from ext.token_generator import TokenGenerator


class RegisterUserController:
    def __init__(self, form_data: dict) -> None:
        self.email: str = form_data['email']
        self.name: str = form_data['name']
        self.password: str = form_data['password']

    def handle_registration(self) -> dict:
        usuario, result = UsuarioController.insert_usuario_on_database(self.name, self.email, self.password)
        if result['status'] == 0:
            UsuarioPapelController.insert_usuario_papel(
                usuario.id, UsuarioPapelController.papeis_list['leitor']
            )

        if result['status'] != 0:
            UsuarioController.delete_usuario(usuario)
            return result

        token_link: str = TokenGenerator.get_token(self.email, f"{RegisterUserVars.salt}{usuario.salt.decode('utf8')}")
        token_email: str = TokenGenerator.get_token(self.email, RegisterUserVars.salt)
        result: dict = MailSender.send_confirmation_email(self.email, token_link, token_email)
        if result['status'] != 0:
            return result

        return MessageStatusGenerator.build_status_success(
            'Um link de confirmação foi enviado para seu e-mail. Você tem 60 minutos para ativar sua conta.'
        )
