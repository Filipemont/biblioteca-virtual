from datetime import datetime
from ext.data_encrypt import DataEncrypt
from ext.database import db


class LivroModel(db.Model):
    __tablename__ = 'tb_livro'
    __table_args__ = {"schema": "db_biblioteca"}

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255))
    autor = db.Column(db.String(255))
    editora = db.Column(db.String(255))
    capa_url = db.Column(db.String(255))
    livro_url = db.Column(db.String(255))
    criado_em = db.Column(db.DateTime(timezone=False), nullable=True, default=datetime.now())
    atualizado_em = db.Column(db.DateTime(timezone=False), nullable=True, default=None, onupdate=lambda: datetime.now())
    usuario = db.relationship("UsuarioLivroModel", back_populates='livro')
