from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class TaskForm(FlaskForm):
    class Meta:
        locales = ["es"]  # mensajes de error en español

    title = StringField("Título", validators=[DataRequired(), Length(max=120)])
    description = TextAreaField("Descripción", validators=[Optional(), Length(max=1000)])
    submit = SubmitField("Guardar")
