from controller.recoverer_user_password.recoverer_user_password_controller import RecovererUserPasswordController
from controller.recoverer_user_password.reset_user_password_controller import ResetUserPasswordController
from flask import Blueprint, Response, flash, redirect, render_template, url_for  # type: ignore
from forms.recoverer_user_password_form import RecovererUserPasswordForm
from forms.reset_user_password_forms import ResetUserPasswordForm


recoverer_user_password_blueprint = Blueprint(
    "recoverer_user_password_blueprint", __name__, template_folder="templates"
)


@recoverer_user_password_blueprint.route("/recoverer_user_password", methods=["GET", "POST"])
def recoverer_user_password() -> Response:
    form = RecovererUserPasswordForm()
    if form.validate_on_submit():
        form_data = {
            'email': form.email.data,
        }

        controller: object = RecovererUserPasswordController(form_data)
        result: dict = controller.handle_recoverer_password()
        flash(result['msg'], result['flash'])
        return redirect(url_for('recoverer_user_password_blueprint.recoverer_user_password'))
    return render_template('recoverer_user_password.html', form=form)


@recoverer_user_password_blueprint.route("/reset_user_password/<token_email>/<token_link>", methods=["GET", "POST"])
def reset_user_password(token_email: str, token_link: str) -> Response:
    email, result = ResetUserPasswordController.valid_token(token_email, token_link)

    if (result['status']) != 0:
        flash(result['msg'], result['flash'])
        return redirect(url_for('login_blueprint.login'))

    form = ResetUserPasswordForm()
    if form.validate_on_submit():
        form_data: dict = {'password': form.password.data, 'email': email}
        print(form_data)
        controller: object = ResetUserPasswordController(form_data)

        result: dict = controller.handle_with_reset()

        flash(result['msg'], result['flash'])
        return redirect(url_for('login_blueprint.login'))

    return render_template('reset_user_password.html', form=form)
