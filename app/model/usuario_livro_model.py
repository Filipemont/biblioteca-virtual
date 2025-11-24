from ext.database import db


class UsuarioLivroModel(db.Model):
    __tablename__ = 'tb_usuario_livro'
    __table_args__ = {"schema": "db_biblioteca"}

    codigo = db.Column(db.Integer, primary_key=True)
    usuario_codigo = db.Column(db.Integer, db.ForeignKey('db_biblioteca.tb_usuario.codigo'))
    livro_codigo = db.Column(db.Integer, db.ForeignKey('db_biblioteca.tb_livro.id'))
    ult_pagina = db.Column(db.Integer)

    usuario = db.relationship("UsuarioModel", back_populates='leituras')
    livro = db.relationship("LivroModel", back_populates='usuario')
