from ext.database import db


class UsuarioPapelModel(db.Model):
    __tablename__ = 'tb_usuario_papel'
    __table_args__ = {"schema": "db_biblioteca"}

    codigo = db.Column(db.Integer, primary_key=True)
    usuario_codigo = db.Column(db.Integer, db.ForeignKey('db_biblioteca.tb_usuario.codigo'))
    papel_codigo = db.Column(db.Integer, db.ForeignKey('db_biblioteca.tb_papel.codigo'))

    usuario = db.relationship("UsuarioModel", back_populates='papeis')
    papel = db.relationship("PapelModel", back_populates='usuarios')
