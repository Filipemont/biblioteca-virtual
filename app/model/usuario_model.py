from datetime import datetime
from ext.data_encrypt import DataEncrypt
from ext.database import db
from flask_login import UserMixin  # type: ignore


class UsuarioModel(db.Model, UserMixin):
    __tablename__ = 'tb_usuario'
    __table_args__ = {"schema": "db_biblioteca"}

    id = db.Column('codigo', db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    email = db.Column(db.String(255))
    senha = db.Column(db.String(32))
    status = db.Column(db.Integer)
    salt = db.Column(db.LargeBinary)
    atualizado_em = db.Column(db.DateTime(timezone=False), nullable=True, default=None, onupdate=lambda: datetime.now())
    papeis = db.relationship("UsuarioPapelModel", back_populates='usuario')
    leituras = db.relationship("UsuarioLivroModel", back_populates='usuario')

    def set_nome(self, nome: str):
        self.nome = DataEncrypt.get_encrypted_aead(nome)

    def get_nome(self) -> str:
        try:
            return DataEncrypt.get_decrypted_aead(self.nome)
        except:
            return None

    def set_email(self, email: str):
        self.email = DataEncrypt.get_encrypted_daead(email)

    def get_email(self) -> str:
        try:
            return DataEncrypt.get_decrypted_daead(self.email)
        except:
            return None

    def has_role(self, role: str) -> bool:
        for usuario_papel in self.papeis:
            if usuario_papel.papel.tipo == role:
                return True
        return False

    def get_status(self):
        if self.status == 1:
            return "Ativo"
        return "Inativo"
