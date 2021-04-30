from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class MorphParsForm(FlaskForm):
    text = TextAreaField('Введите текст:', validators=[DataRequired()], render_kw={"rows": 4})
    check_grammar = BooleanField("Проверить грамматику")
    submit = SubmitField('Проверить')
