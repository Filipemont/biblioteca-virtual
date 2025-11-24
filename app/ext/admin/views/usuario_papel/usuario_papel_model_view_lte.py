import psycopg2  # type: ignore
import unicodedata
from ext.admin.views.base_model_view_lte import BaseModelViewLTE
from ext.admin.views.usuario_papel.custom_papel_from_usuario_papel_filter import CustomPapelFromUsuarioPapelFilter
from ext.admin.views.usuario_papel.custom_usuario_papel_filter import CustomUsuarioPapelFilter
from flask import Response, current_app, flash, redirect, render_template, request, url_for  # type: ignore
from flask_admin._compat import text_type  # type: ignore
from flask_admin.babel import gettext  # type: ignore
from flask_admin.base import expose  # type: ignore
from flask_admin.form import FormOpts  # type: ignore
from flask_admin.form.widgets import Select2Widget # type: ignore
from flask_admin.helpers import get_redirect_target  # type: ignore
from flask_login import current_user  # type: ignore
from flask_sqlalchemy import BaseQuery  # type: ignore
from model.papel_model import PapelModel
from model.usuario_model import UsuarioModel
from sqlalchemy import case  # type: ignore
from sqlalchemy.exc import IntegrityError, SQLAlchemyError  # type: ignore
from wtforms_sqlalchemy.fields import QuerySelectField  # type: ignore


class UsuarioPapelModelViewLTE(BaseModelViewLTE):
    column_display_pk: bool = True
    column_list: list = ['nome', 'email', 'papel']
    column_filters: list = [
        CustomUsuarioPapelFilter('usuario.nome', name="Nome"),
        CustomUsuarioPapelFilter('usuario.email', name="Email"),
        CustomPapelFromUsuarioPapelFilter('papel.tipo', name="Papeis"),
    ]
    column_formatters: dict = {
        'nome': lambda v, c, m, p: m.usuario.get_nome().title() if m.usuario and m.usuario.get_nome() else "",
        'email': lambda v, c, m, p: m.usuario.get_email() if m and m.usuario.get_email() else "",
        'papel': lambda v, c, m, p: m.papel.tipo,
    }
    column_formatters_detail: dict = {
        'nome': lambda v, c, m, p: m.usuario.get_nome().title() if m.usuario and m.usuario.get_nome() else "",
        'email': lambda v, c, m, p: m.usuario.get_email() if m and m.usuairo.get_email() else "",
        'papel': lambda v, c, m, p: m.papel.tipo,
    }

    can_edit: bool = False
    can_delete: bool = True
    create_modal: bool = False
    can_create: bool = True
    can_view_details: bool = False

    form_overrides: dict = {'usuario': QuerySelectField, 'papel': QuerySelectField}

    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs) -> Response:
        return render_template('error.html', error_str='Usuário não possui permissão', error_code='403')

    def create_model(self, form) -> redirect:
        try:
            return super().create_model(form)
        except psycopg2.errors.RaiseException:
            flash("Erro ao atribuir o papel. Este usuário não pode receber o papel de (Coloque aqui o papel).", "error")
            return redirect(url_for('admin.index'))
        except SQLAlchemyError:
            flash("Erro ao atribuir o papel. Este usuário não pode receber o papel de (Coloque aqui o papel)", "error")
            return redirect(url_for('admin.index'))
        except Exception:
            flash("Erro ao atribuir o papel. Este usuário não pode receber o papel de (Coloque aqui o papel)", "error")
            return redirect(url_for('admin.index'))
        except psycopg2.errors.UniqueViolation:
            flash("Erro ao atribuir o papel. Este usuário ja possui este papel.", "error")
            return redirect(url_for('admin.index'))

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self) -> redirect:
        return_url: str = get_redirect_target() or self.get_url('.index_view')

        if not self.can_create:
            return redirect(return_url)

        form = self.create_form()
        if not hasattr(form, '_validated_ruleset') or not form._validated_ruleset:
            self._validate_form_instance(ruleset=self._form_create_rules, form=form)

        if self.validate_form(form):
            model = self.create_model(form)
            if model:
                if '_add_another' in request.form:
                    flash('Papel concedido com sucesso.', 'success')
                    return redirect(request.url)
                elif '_continue_editing' in request.form:
                    flash('Papel concedido com sucesso', 'success')
                    if model is not True:
                        url = self.get_url('.edit_view', id=self.get_pk_value(model), url=return_url)
                    else:
                        url = return_url
                    return redirect(url)
                else:
                    try:
                        if model.codigo:
                            flash('Papel concedido com sucesso', 'success')
                    except AttributeError:
                        pass
                    return redirect(self.get_save_return_url(model, is_created=True))

        form_opts: object = FormOpts(widget_args=self.form_widget_args, form_rules=self._form_create_rules)

        if self.create_modal and request.args.get('modal'):
            template = self.create_modal_template
        else:
            template = self.create_template

        return self.render(template, form=form, form_opts=form_opts, return_url=return_url)

    def handle_view_exception(self, exc) -> bool:
        if isinstance(exc, IntegrityError):
            if current_app.config.get(
                'ADMIN_RAISE_ON_INTEGRITY_ERROR', current_app.config.get('ADMIN_RAISE_ON_VIEW_EXCEPTION')
            ):
                raise
            else:
                message: str = gettext('Integrity error. %(message)s', message=text_type(exc))
                if 'usuario_papel_unico' in message:
                    flash(gettext('O usuário já possui este papel.', message=text_type(exc)), 'error')
                elif 'psycopg2.errors.NotNullViolation' in message:
                    flash(
                        gettext('Preencha os dois campos antes de enviar a solicitação.', message=text_type(exc)),
                        'error',
                    )
                else:
                    flash(gettext('Integrity error. %(message)s', message=text_type(exc)), 'error')
            return True

    def get_sorted_users():
        query: BaseQuery = UsuarioModel.query
        user_names_and_ids = []
        users_sorted_ids_by_sorted_names = []
        user_sorted_names = []
        for record in query:
            if record.get_nome():
                nome_normalizado = unicodedata.normalize('NFD', record.get_nome())
                nome_sem_acento = ''.join(c for c in nome_normalizado if not unicodedata.combining(c))
                user_sorted_names.append(nome_sem_acento.lower())
                user_names_and_ids.append({nome_sem_acento.lower(): record.id})
        user_sorted_names.sort()

        for name in user_sorted_names:
            for user in user_names_and_ids:
                if name in user:
                    users_sorted_ids_by_sorted_names.append(user[name])
        order_by_case = case(
            [(UsuarioModel.id == user_id, index) for index, user_id in enumerate(users_sorted_ids_by_sorted_names)],
            else_=len(users_sorted_ids_by_sorted_names),
        )
        query = query.filter(UsuarioModel.id.in_(users_sorted_ids_by_sorted_names))
        query = query.order_by(order_by_case)
        return query

    form_args = {
        'usuario': {
            'query_factory': get_sorted_users,
            'allow_blank': False,
            'get_label': lambda usuario: f"{usuario.get_nome()} - {usuario.get_email()}",
            'widget': Select2Widget(),
        },
        'papel': {'query_factory': lambda: PapelModel.query.all(), 'allow_blank': False, 'get_label': 'tipo'},
    }
