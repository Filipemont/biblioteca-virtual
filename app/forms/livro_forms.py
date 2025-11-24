from flask_wtf import FlaskForm  # type: ignore
from flask_wtf.file import FileAllowed  # type: ignore
from wtforms import FileField, StringField, SubmitField  # type: ignore
from wtforms.validators import DataRequired, Length, Optional  # type: ignore


class LivroForm(FlaskForm):
    titulo = StringField('Titulo do livro', validators=[DataRequired(), Length(max=50)])
    autor = StringField('Autor', validators=[Optional(), Length(max=50)])
    editora = StringField('Editora', validators=[DataRequired(), Length(max=50)])
    capa = FileField(
        'Imagem da capa do livro', validators=[DataRequired(), FileAllowed(["jpeg", "jpg", "png"], "Image only!")]
    )
    livro = FileField(
        'Livro (arquivo no formato pdf)', validators=[DataRequired(), FileAllowed(["pdf"], "PDF only!")]
    )
    submit = SubmitField('Salvar')

