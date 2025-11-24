from controller.usuario_papel_controller import UsuarioPapelController
from controller.login.login_auth_controller import LoginAuthController
from controller.login.login_controller import LoginController
from flask import Blueprint, Response, flash, redirect, render_template, request, session, url_for  # type: ignore
from flask_login import current_user, login_required, login_user, logout_user  # type: ignore
from forms.login_auth_form import LoginAuthForm
from forms.login_form import LoginForm


login_blueprint = Blueprint("login_blueprint", __name__, template_folder="templates")


@login_blueprint.route("/login", methods=["GET", "POST"])
def login() -> Response:
    if current_user.is_authenticated:
        return redirect(url_for("area_admin_blueprint.area_admin"))
    form: object = LoginForm()
    if form.validate_on_submit():
        user_mail: str = form.email.data
        user_password: str = form.password.data
        controller: object = LoginController(user_mail, user_password)
        if not controller.check_usr(user_password):
            flash(controller.result['msg'], controller.result['flash'])
            return redirect(url_for("login_blueprint.login"))
        controller._set_token_id()
        return redirect(
            url_for(
                'login_blueprint.login_auth',
                token_get=controller.token_get,
                token_post=controller.token_post,
                parameter_token=controller.token_parameter,
            )
        )
    return render_template('login.html', form=form, next=request.args.get("next"))


@login_blueprint.route("/login/auth/<token_get>/<token_post>/<parameter_token>", methods=["GET", "POST"])
def login_auth(token_get: str, token_post: str, parameter_token: str) -> Response:
    form: object = LoginAuthForm()
    controller: object = LoginAuthController()
    if request.method == 'GET':
        controller.handle_autentication(token_get, 1 / 10, request.method, parameter_token)
        if controller.id:
            controller.send_mail_auth()
            return render_template('login_auth.html', form=form, next=request.args.get("next"))

    if request.method == 'POST':
        if form.validate_on_submit():
            code = form.codigo.data
            controller.handle_autentication(token_post, 60, request.method, parameter_token)
            if controller.result['status'] == 0 and controller.validate_token(code):
                usuario = controller._load_user()
                login_user(usuario)
                session.permanent = True
                if UsuarioPapelController().check_usuario_papel(current_user.papeis):
                    if any(p.papel.tipo == 'admin' for p in current_user.papeis):
                        return redirect(url_for('admin.index'))
                    return redirect(url_for("web_blueprint.homepage"))
                flash('Usuário sem permissão de acesso ao sistema, contate o administrador.', 'error')
                logout_user()
                return redirect(url_for("login_blueprint.login"))
            flash(controller.result['msg'], controller.result['flash'])
            return redirect(url_for("login_blueprint.login"))

    flash(controller.result['msg'], controller.result['flash'])
    return redirect(url_for('login_blueprint.login'))


@login_blueprint.route('/logout')
@login_required
def logout() -> Response:
    logout_user()
    return redirect(url_for('login_blueprint.login'))
