from ext.database import db
from ext.message_status_generator import MessageStatusGenerator
from model.usuario_papel_model import UsuarioPapelModel


class UsuarioPapelController:
    papeis_list: dict = {
        "leitor": 1,
        "admin": 2,
    }

    @staticmethod
    def insert_usuario_papel(usuario_codigo: str, papel_codigo: str) -> dict:
        usuario_papel: object = UsuarioPapelModel(usuario_codigo=usuario_codigo, papel_codigo=papel_codigo)
        try:
            db.session.add(usuario_papel)
            db.session.commit()
            return MessageStatusGenerator.build_status_success()
        except Exception:
            db.session.rollback()
            return MessageStatusGenerator.build_status_error('Erro ao criar o papel do usuário')

    @staticmethod
    def check_usuario_papel(papel_codigo: str) -> bool:
        papel_list_values: list = UsuarioPapelController.papeis_list.values()
        for papel in papel_codigo:
            if papel.papel_codigo in papel_list_values:
                return True
        return False
