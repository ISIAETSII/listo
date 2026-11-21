from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    class Meta:
        locales = ["es"]  # mensajes de error en español (traducciones que trae WTForms)

    name = StringField("Nombre", validators=[DataRequired(), Length(max=80)])
    email = EmailField("Correo electrónico", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=6, max=128)])
    confirm = PasswordField(
        "Repite la contraseña",
        validators=[
            DataRequired(),
            EqualTo("password", message="Las contraseñas no coinciden."),
        ],
    )
    submit = SubmitField("Crear cuenta")


class LoginForm(FlaskForm):
    class Meta:
        locales = ["es"]

    email = EmailField("Correo electrónico", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    remember = BooleanField("Recordarme")
    submit = SubmitField("Entrar")
