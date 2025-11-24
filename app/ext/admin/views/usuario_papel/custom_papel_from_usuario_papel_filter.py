from flask_admin.contrib.sqla.filters import BaseSQLAFilter  # type: ignore
from flask_sqlalchemy import BaseQuery  # type: ignore
from model.usuario_papel_model import UsuarioPapelModel


class CustomPapelFromUsuarioPapelFilter(BaseSQLAFilter):
    def apply(self, query: BaseQuery, value: str, alias=None) -> BaseQuery:
        matching_ids: list = []
        for record in query:
            papel: object = getattr(record, 'papel', None)
            if papel is None:
                continue
            if papel and value.lower() in papel.tipo.lower():
                matching_ids.append(record.papel_codigo)
        return query.filter(UsuarioPapelModel.papel_codigo.in_(matching_ids))

    def operation(self) -> str:
        return "contém"
