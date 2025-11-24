from ext.database import db


class PapelModel(db.Model):
    __tablename__ = 'tb_papel'
    __table_args__ = {"schema": "db_biblioteca"}

    codigo = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    descricao = db.Column(db.String(255))

    usuarios = db.relationship("UsuarioPapelModel", back_populates='papel')
