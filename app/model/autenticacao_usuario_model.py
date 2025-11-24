from ext.database import db


class AutenticacaoModel(db.Model):
    __tablename__ = 'tb_codigo_autenticacao'
    __table_args__ = {"schema": "db_biblioteca"}

    codigo = db.Column(db.Integer, primary_key=True)
    horario_chave = db.Column(db.Integer)
    usuario_codigo = db.Column(db.Integer, db.ForeignKey('db_biblioteca.tb_usuario.codigo'), unique=True)
    secret = db.Column(db.String(32))

    usuario_rel = db.relationship("UsuarioModel", backref="autenticacao")
