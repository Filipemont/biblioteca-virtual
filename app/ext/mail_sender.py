import os
import smtplib
from ext.message_status_generator import MessageStatusGenerator
from flask import url_for  # type: ignore
from flask_mail import Mail, Message  # type: ignore


class MailSender:
    mail: object = Mail()

    @staticmethod
    def init_app(app) -> None:
        app.config.update(
            MAIL_SERVER=os.getenv('MAIL_SERVER'),
            MAIL_PORT=os.getenv('MAIL_PORT'),
            MAIL_USE_TLS=True,
            MAIL_USE_SSL=False,
            MAIL_USERNAME=os.getenv('EMAIL'),      
            MAIL_PASSWORD=os.getenv('SENHA'),        
            MAIL_DEFAULT_SENDER=("Biblioteca Virtual", os.getenv('EMAIL')),
        )
        MailSender.mail.init_app(app)

    @staticmethod
    def __send_link_email(
        email: str, token_link: str, token_email: str, message: str,
        link_message: str, url_blueprint: str, footer: str
    ) -> dict:
        link: str = url_for(url_blueprint, token_link=token_link, token_email=token_email, _external=True)
        msg: object = Message(
            subject=message,
            recipients=[email],
        )
        msg.body = f"{link_message}: {link}\n\n{footer}"
        return MailSender.__send_email(msg)

    @staticmethod
    def __send_email(msg: object) -> dict:
        try:
            MailSender.mail.send(msg)
            return MessageStatusGenerator.build_status_success()
        except smtplib.SMTPAuthenticationError:
            return MessageStatusGenerator.build_status_error(
                "Falha de autenticação SMTP. Verifique usuário/senha do e-mail."
            )
        except smtplib.SMTPException as e:
            return MessageStatusGenerator.build_status_error(f"Erro ao enviar e-mail: {str(e)}")

    @staticmethod
    def send_confirmation_email(email: str, token_link: str, token_email: str) -> dict:
        return MailSender.__send_link_email(
            email,
            token_link,
            token_email,
            "Confirme seu cadastro na biblioteca virtual",
            "Tempo para ativação: 60 minutos.\n\nPor favor, clique no link para ativar sua conta",
            "register_user_blueprint.confirm_email",
            MailSender.__get_email_footer("link"),
        )

    @staticmethod
    def send_recoverer_password_email(email: str, token_link: str, token_email: str) -> dict:
        return MailSender.__send_link_email(
            email,
            token_link,
            token_email,
            "Recuperar senha na biblioteca virtual",
            "Por favor, clique no link para criar uma nova senha",
            "recoverer_user_password_blueprint.reset_user_password",
            MailSender.__get_email_footer("link"),
        )

    @staticmethod
    def __get_email_footer(email_object) -> str:
        return (
            f"\n\nSe você não solicitou este {email_object} ou acredita que houve algum erro,\n"
            f"por favor, desconsidere este e-mail. Para sua segurança, este {email_object} não deve ser\n"
            "compartilhado com ninguém. Caso tenha dificuldades ou precise de suporte, entre em contato conosco.\n\n"
        )

    @staticmethod
    def send_confirmation_login(email: str, nome: str, token: str) -> dict:
        msg = Message(
            subject="Seu Código de Verificação - Ação Necessária",
            recipients=[email],
        )
        msg.body = (
            f"Olá {nome},\n"
            "Para continuar com a sua solicitação de acesso, por motivos de segurança, é necessário confirmar"
            " sua identidade.\n\n"
            f"Seu código de verificação é: {token}\n\n"
            "Este código é válido por 60 segundos e deverá ser utilizado para concluir o processo de autenticação."
            f"{MailSender.__get_email_footer('link')}"
        )
        return MailSender.__send_email(msg)
