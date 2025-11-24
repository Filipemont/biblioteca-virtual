import hashlib
from ext.admin.views.base_model_view_lte import BaseModelViewLTE
from ext.data_encrypt import DataEncrypt
from ext.date_utils import DateUtils
from ext.hash_generator import HashGenerator
from flask import Response, render_template  # type: ignore
from flask_login import current_user  # type: ignore
from wtforms.fields import PasswordField, SelectField  # type: ignore


class UsuarioModelViewLTE(BaseModelViewLTE):
    can_edit: bool = True
    can_delete: bool = True
    can_create: bool = True
    can_view_details: bool = False

    column_exclude_list: list = ['senha', 'salt']
    form_excluded_columns: list = ['senha', 'salt']
    column_details_exclude_list: list = ['senha', 'salt']
    column_export_exclude_list: list = ['senha', 'salt']

    column_formatters: dict = {
        'nome': lambda v, c, m, p: m.get_nome(),
        'email': lambda v, c, m, p: m.get_email(),
        'status': lambda v, c, m, p: m.get_status(),
        'senha': lambda v, c, m, p: m.senha,
        'atualizado_em': lambda v, c, m, p: DateUtils.format_datetime_to_brazilian(m.atualizado_em),
    }

    form_columns: list = ['nome', 'email', 'senha', 'status']

    form_create_rules: list = ['nome', 'email', 'senha', 'status']

    form_edit_rules: list = [
        'status',
    ]
    form_overrides: dict = {'status': SelectField, 'senha': PasswordField}

    form_args: dict = {
        'status': {'label': 'Status do Usuário', 'choices': [(1, 'Ativo'), (0, 'Inativo')], 'coerce': int}
    }

    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs) -> Response:
        return render_template('error.html', error_str='Usuário não possui permissão', error_code='403')

    def on_model_change(self, form, model, is_created):
        if is_created:
            if model.email:
                model.email = DataEncrypt.get_encrypted_daead(model.email)
            if model.nome:
                model.nome = DataEncrypt.get_encrypted_aead(model.nome)
            if model.senha:
                password_bytes = model.senha.encode('utf-8')
                sha256_hash = hashlib.sha256(password_bytes)
                model.salt, model.senha = HashGenerator.generate_hashed_password(f"{sha256_hash.hexdigest()}A#")
                model.senha = model.senha.decode('utf-8')
