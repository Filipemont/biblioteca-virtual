from flask_wtf import FlaskForm  # type: ignore
from wtforms import StringField, SubmitField  # type: ignore
from wtforms.validators import DataRequired  # type: ignore


class LoginAuthForm(FlaskForm):
    codigo = StringField(
        'Codigo de verificação:',
        validators=[DataRequired()],
        render_kw={"placeholder": "Entre com o código enviado para seu email. Você tem 60 segundos. "},
    )
    submit = SubmitField('Confirmar')
