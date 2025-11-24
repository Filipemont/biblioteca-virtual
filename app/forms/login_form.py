from flask_wtf import FlaskForm, RecaptchaField  # type: ignore
from wtforms import EmailField, PasswordField, SubmitField  # type: ignore
from wtforms.validators import DataRequired, Email  # type: ignore


class LoginForm(FlaskForm):
    email = EmailField(
        'Email:',
        validators=[DataRequired(), Email(message="Por favor, insira um endereço de e-mail válido.")],
        render_kw={"placeholder": "Entre com o Email"},
    )
    password = PasswordField('Senha:', validators=[DataRequired()], render_kw={"placeholder": "Entre com a senha"})
    # recaptcha = RecaptchaField()
    submit = SubmitField('Login')
