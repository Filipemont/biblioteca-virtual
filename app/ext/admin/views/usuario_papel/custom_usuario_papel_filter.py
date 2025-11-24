from flask_admin.contrib.sqla.filters import BaseSQLAFilter  # type: ignore
from flask_sqlalchemy import BaseQuery  # type: ignore
from model.usuario_papel_model import UsuarioPapelModel


class CustomUsuarioPapelFilter(BaseSQLAFilter):
    def apply(self, query, value, alias=None) -> BaseQuery:
        column: str = self.column
        matching_ids: list = []
        for record in query:
            usuario: object = getattr(record, 'usuario', None)
            if usuario is None:
                continue
            if column == 'usuario.email':
                decrypted_nome: str = usuario.get_email()
            else:
                decrypted_nome: str = usuario.get_nome()
            if decrypted_nome and value.lower() in decrypted_nome.lower():
                matching_ids.append(record.usuario_codigo)
        return query.filter(UsuarioPapelModel.usuario_codigo.in_(matching_ids))

    def operation(self) -> str:
        return "contém"
