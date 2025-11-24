from flask import Blueprint, Response, render_template, jsonify
from flask_login import current_user  # type: ignore
from controller.livro_controller import LivroController



web_blueprint = Blueprint("web_blueprint", __name__, template_folder="templates")


@web_blueprint.route("/")
def homepage() -> Response:
    if current_user.is_authenticated:
        livros = LivroController.get_all_livros_decrypted_dict()
        return render_template("livros.html", user=current_user, livros=livros)
    else:
        capas = LivroController.get_random_book_covers()
        return render_template("homepage.html", capas=capas)

