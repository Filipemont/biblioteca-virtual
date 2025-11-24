from ext.data_encrypt import DataEncrypt
from ext.database import db
from ext.hash_generator import HashGenerator
from ext.message_status_generator import MessageStatusGenerator
from model.usuario_model import UsuarioModel
from sqlalchemy.exc import IntegrityError  # type: ignore


class UsuarioController:
    @staticmethod
    def check_email_exist(email: str) -> bool:
        usuario = UsuarioController.get_usuario_by_email(email)
        if usuario:
            return True
        return False

    @staticmethod
    def get_usuario_by_email(email: str) -> UsuarioModel:
        usuario = UsuarioModel.query.filter_by(email=DataEncrypt.get_encrypted_daead(email)).first()
        return usuario

    @staticmethod
    def get_usuario_by_codigo(codigo: str) -> UsuarioModel:
        return UsuarioModel.query.get(codigo)

    @staticmethod
    def delete_usuario(usuario: UsuarioModel) -> None:
        db.session.delete(usuario)
        db.session.commit()

    @staticmethod
    def insert_usuario_on_database(nome: str, email: str, senha: str) -> tuple:
        salt, hashed_password = HashGenerator.generate_hashed_password(senha)
        usuario: object = UsuarioModel(senha=hashed_password.decode('utf-8'), salt=salt, status=0)
        usuario.set_nome(nome)
        usuario.set_email(email)
        try:
            db.session.add(usuario)
            db.session.commit()
            return usuario, MessageStatusGenerator.build_status_success()
        except IntegrityError:
            db.session.rollback()
            return usuario, MessageStatusGenerator.build_status_error(
                'Este email já está cadastrado. Por favor, use um email diferente.'
            )
        except Exception:
            db.session.rollback()
            return usuario, MessageStatusGenerator.build_status_error('Erro ao criar novo usuário')

    @staticmethod
    def update_usuario_senha_by_email(email: str, senha: str) -> dict:
        try:
            usuario: object = UsuarioController.get_usuario_by_email(email)
            if usuario is None:
                return MessageStatusGenerator.build_status_error('Erro ao atualizar senha')
            salt, hashed_password = HashGenerator.generate_hashed_password(senha)
            usuario.senha = hashed_password.decode('utf-8')
            usuario.salt = salt
            db.session.commit()
            return MessageStatusGenerator.build_status_success()
        except Exception:
            db.session.rollback()
            return MessageStatusGenerator.build_status_error('Erro ao atualizar senha')
