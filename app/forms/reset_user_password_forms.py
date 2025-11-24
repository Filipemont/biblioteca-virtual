from flask_wtf import FlaskForm, RecaptchaField  # type: ignore
from forms.forms_utils import FormsUtils
from wtforms import PasswordField, SubmitField  # type: ignore
from wtforms.validators import DataRequired, Length, ValidationError  # type: ignore


class ResetUserPasswordForm(FlaskForm):
    password = PasswordField('Indique sua nova senha:', validators=[DataRequired(), Length(min=1, max=70)])
    confirm_password = PasswordField('Confirme sua nova senha:', validators=[DataRequired(), Length(min=1, max=70)])
    # recaptcha = RecaptchaField()
    submit = SubmitField('Enviar')

    def validate_confirm_password(self, confirm_password):
        if confirm_password.data != self.password.data:
            raise ValidationError('As senhas devem ser iguais.')

    def validate_password(self, password):
        return FormsUtils.validate_password(password)
