from controller.livro_controller import LivroController
from flask import Response, flash, redirect, render_template, request, send_file, url_for  # type: ignore
from flask_admin import BaseView, expose  # type: ignore
from flask_login import current_user  # type: ignore
from forms.livro_forms import LivroForm
from urllib.parse import unquote

class LivroModelViewLTE(BaseView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs) -> Response:
        return render_template('error.html', error_str='Usuário não possui permissão', error_code='403')

    @expose("/", methods=["GET"])
    def listar_livros_criados(self) -> Response:
        livros: list = LivroController.get_all_livros_dict()
        if not livros:
            return self.render("area_admin/area_gestor/livro/livro.html", livros=None)
        return self.render("area_admin/area_gestor/livro/livro.html", livros=livros)

    @expose("/criar-livro", methods=["GET", "POST"])
    def criar_livro(self) -> Response:
        form: object = LivroForm()
        if request.method == "POST" and form.validate_on_submit():
            controller: object = LivroController(request.form, request.files)
            result: dict = controller.save_livro_on_db()
            if 'Sucesso' in result.get('flash'):
                controller.create_documentos_list()
                controller.create_documentos_on_bucket_and_db()
                if 'success' in controller.result.get('flash'):
                    return redirect(url_for('livros.listar_livros_criados'))
            flash(result['msg'], result['flash'])
            return self.render("area_admin/area_gestor/livro/livro_create.html", form=form)
        return self.render("area_admin/area_gestor/livro/livro_create.html", form=form)

    @expose("/editar-livro", methods=["GET", "POST"])
    def editar_livro(self) -> Response:
        id_livro = request.args.get('id')
        livro: dict = LivroController().get_livro_dict_by_codigo(id_livro)
        form: object = LivroForm()
        if request.method == "POST" and form.validate_on_submit():
            controller: object = LivroController(request.form, request.files)
            controller.set_livro_id(id_livro)
            controller.create_documentos_list()
            controller.create_documentos_on_bucket_and_db()
            result = controller.get_result()                  
            flash(result['msg'], result['flash'])
            if 'success' in result.get('flash'):
                controller.update_livro()
                return redirect(url_for('livros.listar_livros_criados'))
            return self.render(
                "area_admin/area_gestor/livro/livro_edit.html",
                livro=livro,
                form=form,
            )
        return self.render("area_admin/area_gestor/livro/livro_edit.html", livro=livro, form=form)

    @expose("/download-doc/<path:path>", methods=["GET"])
    def download_minio(path: str, cls=None) -> Response:
        print('path:')
        print(path)
        decoded_path = unquote(path)
        document_data: Response = LivroController.get_minio_file(decoded_path)
        download_name: str = LivroController.get_document_perfil_name(path)
        return send_file(document_data, as_attachment=True, download_name=download_name)
    
    @expose("/delete-livro", methods=["GET"])
    def delete_livro(self):
        id_livro = request.args.get('id')
        controller = LivroController()
        controller.delete_livro_by_id(id_livro)
        result = controller.get_result()
        flash(result['msg'], result['flash'])
        if 'success' in result.get('flash'):
            controller.delete_book_from_minio(id_livro)
            return redirect(url_for('livros.listar_livros_criados'))
