from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class MorphParsForm(FlaskForm):
    text = TextAreaField('Текст', validators=[DataRequired()], render_kw={"rows": 8})
    check_grammar = BooleanField("Проверить грамматику")
    submit = SubmitField('Проверить')
