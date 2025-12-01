from flask import Blueprint, render_template, escape
from utils.minio_utils import MinioUtil
from controller.livro_controller import LivroController
from flask_login import login_required # type: ignore

leitura_view = Blueprint("leitura_view", __name__, url_prefix="/leitura")


@leitura_view.route("/<path:id_livro>")
@login_required
def ler_livro(id_livro):
    minio_util = MinioUtil()
    try:
        livro = LivroController.get_livro_decrypted_by_codigo(escape(id_livro))
        url_temporaria = minio_util.get_minio_url(livro.get("livro_url"))
        return render_template("leitura.html", livro_link=url_temporaria)
    except Exception as e:
        return "File not found", 404