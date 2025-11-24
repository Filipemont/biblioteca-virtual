from ext.admin.views.usuario_model_view_lte import UsuarioModelViewLTE
from ext.admin.views.usuario_papel.usuario_papel_model_view_lte import UsuarioPapelModelViewLTE
from ext.admin.views.livro.livro_model_view_lte import LivroModelViewLTE
from ext.database import db
from flask import Response  # type: ignore
from flask_admin import Admin, AdminIndexView, expose  # type: ignore
from flask_admin.menu import MenuLink  # type: ignore
from flask_login import login_required  # type: ignore
from model.usuario_model import UsuarioModel
from model.usuario_papel_model import UsuarioPapelModel


class AdminIndexViewLTE(AdminIndexView):
    @expose("/", methods=["GET", "POST"])
    @login_required
    def index(self) -> Response:
        return self.render("area_admin/painel_principal.html")


admin = Admin(
    name="Biblioteca Unich Admin",
    base_template="area_admin/master.html",
    template_mode="bootstrap4",
    index_view=AdminIndexViewLTE(),
)

admin.add_category(name="Controle de Acesso", class_name="fas fa-user-shield")
admin.add_category(name="Controle de Livros", class_name="fas fa-book-open")


admin.add_view(
    UsuarioModelViewLTE(
        UsuarioModel,
        db.session,
        category="Controle de Acesso",
        endpoint="usuarios",
        name="Usuários",
        menu_icon_type="fa",
        menu_icon_value="fa-user",
    )
)
admin.add_view(
    UsuarioPapelModelViewLTE(
        UsuarioPapelModel,
        db.session,
        name="Papel dos Usuários",
        menu_icon_type="fa",
        menu_class_name="btn-secondary",
        menu_icon_value="fa-pencil-square-o",
        category="Controle de Acesso",
        endpoint='usuariopapel',
    )
)
admin.add_view(
    LivroModelViewLTE(
        name="Livros",
        menu_icon_type="fa",
        menu_class_name="btn-secondary",
        menu_icon_value="fa-book",
        category="Controle de Livros",
        endpoint='livros',
    )
)


admin.add_link(MenuLink(name="Logout", url="/logout"))
