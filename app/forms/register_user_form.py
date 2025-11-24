from flask_wtf import FlaskForm, RecaptchaField  # type: ignore
from forms.forms_utils import FormsUtils
from wtforms import EmailField, PasswordField, StringField, SubmitField  # type: ignore
from wtforms.validators import DataRequired, Email, Length, ValidationError  # type: ignore


class RegisterUserForm(FlaskForm):
    name = StringField('Indique seu nome:', validators=[DataRequired(), Length(min=1, max=70)])
    email = EmailField(
        'Indique seu email:',
        validators=[
            DataRequired(),
            Length(min=1, max=70),
            Email(message="Por favor, insira um endereço de e-mail válido."),
        ],
    )
    confirm_email = EmailField(
        'Confirme seu email:',
        validators=[
            DataRequired(),
            Length(min=1, max=70),
            Email(message="Por favor, insira um endereço de e-mail válido."),
        ],
    )
    password = PasswordField('Indique sua senha:', validators=[DataRequired(), Length(min=1, max=70)])
    confirm_password = PasswordField('Confirme sua senha:', validators=[DataRequired(), Length(min=1, max=70)])
    submit = SubmitField('Enviar')

    def validate_confirm_email(self, confirm_email: object) -> ValidationError:
        if confirm_email.data != self.email.data:
            raise ValidationError('Os endereços de e-mail devem ser iguais.')

    def validate_confirm_password(self, confirm_password: object) -> ValidationError:
        if confirm_password.data != self.password.data:
            raise ValidationError('As senhas devem ser iguais.')

    def validate_password(self, password: object) -> ValidationError:
        return FormsUtils.validate_password(password)
