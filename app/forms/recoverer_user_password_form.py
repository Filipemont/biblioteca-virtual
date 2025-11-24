from flask_wtf import FlaskForm, RecaptchaField  # type: ignore
from wtforms import EmailField, SubmitField  # type: ignore
from wtforms.validators import DataRequired, Email, Length  # type: ignore


class RecovererUserPasswordForm(FlaskForm):
    email = EmailField(
        'Indique seu email para recuperar a senha da sua conta:',
        validators=[
            DataRequired(),
            Length(min=1, max=70),
            Email(message="Por favor, insira um endereço de e-mail válido."),
        ],
    )
    # recaptcha = RecaptchaField()
    submit = SubmitField('Enviar')
