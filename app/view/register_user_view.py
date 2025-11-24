from controller.register_user.confirm_email_controller import ConfirmEmailController
from controller.register_user.register_user_controller import RegisterUserController
from flask import Blueprint, Response, flash, redirect, render_template, url_for, request  # type: ignore
from forms.register_user_form import RegisterUserForm


register_user_blueprint = Blueprint("register_user_blueprint", __name__, template_folder="templates")


@register_user_blueprint.route("/register_user", methods=["GET", "POST"])
def register_user() -> Response:
    form: object = RegisterUserForm()
    if form.validate_on_submit():
        form_data: dict = {'name': form.name.data, 'email': form.email.data, 'password': form.password.data}
        controller: object = RegisterUserController(form_data)
        result: dict = controller.handle_registration()

        if result['status'] == 0:
            flash(result['msg'], result['flash'])
            return redirect(url_for('login_blueprint.login'))
        else:
            flash(result['msg'], result['flash'])
            return redirect(url_for('register_user_blueprint.register_user'))
    return render_template('register_user.html', form=form)


@register_user_blueprint.route('/confirm_email/<token_email>/<token_link>')
def confirm_email(token_email: str, token_link: str) -> Response:
    result: dict = ConfirmEmailController.valid_token(token_email, token_link)
    flash(result['msg'], result['flash'])
    return redirect(url_for('login_blueprint.login'))
