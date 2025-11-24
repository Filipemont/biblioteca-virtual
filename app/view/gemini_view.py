from flask import Blueprint, request, jsonify, render_template
from controller.gemini_controller import GeminiController
from flask_login import login_required # type: ignore


gemini_bp = Blueprint('gemini_bp', __name__)

@gemini_bp.route('/resumo', methods=['POST'])
@login_required
def get_resumo_livro():
    data = request.get_json()
    if not data or 'nome_do_livro' not in data:
        return jsonify({"erro": "O campo 'nome_do_livro' é obrigatório no corpo da requisição."}), 400

    nome_do_livro = data.get('nome_do_livro')
    resumo = GeminiController.get_gemini_resume(nome_do_livro)
    return jsonify(resumo)


@gemini_bp.route('/ler-resumo', methods=['GET'])
@login_required
def render_resumo_page():
    return render_template('resumo_gemini.html')
