from ext.database import db
from model.autenticacao_usuario_model import AutenticacaoModel


class AutenticacaoController:
    def set_autenticacao(horario: str, codigo_usuario: str, secret: str) -> None:
        autenticacao: object = AutenticacaoModel(horario_chave=horario, usuario_codigo=codigo_usuario, secret=secret)
        check: object = AutenticacaoController.get_autenticacao_by_codigo_usuario(codigo_usuario)
        try:
            if check:
                check.horario_chave = horario
                check.secret = secret
                db.session.commit()
            else:
                db.session.add(autenticacao)
                db.session.commit()
        except Exception:
            db.session.rollback()

    def get_autenticacao_by_codigo_usuario(codigo_usuario: str) -> AutenticacaoModel:
        autenticacao: object = AutenticacaoModel.query.filter_by(usuario_codigo=codigo_usuario).first()
        return autenticacao

    def get_usuario_salt_by_codigo_usuario(codigo_usuario: str) -> str:
        autenticacao: object = AutenticacaoModel.query.filter_by(codigo_usuario=codigo_usuario).first()
        if not autenticacao:
            return None
        usuario_salt: str = autenticacao.usuario_rel.salt
        return usuario_salt
