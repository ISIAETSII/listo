from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
import re

DNI_LETTERS = "TRWAGMYFPDXBNJZSQVHLCKE" # la letra es la del resto de dividir entre 23


class RegisterForm(FlaskForm):
    class Meta:
        locales = ["es"]  # mensajes de error en español (traducciones que trae WTForms)

    name = StringField("Nombre", validators=[DataRequired(), Length(max=80)])
    email = EmailField("Correo electrónico", validators=[DataRequired(), Email(), Length(max=120)])
    dni = StringField("DNI", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=6, max=128)])
    confirm = PasswordField(
        "Repite la contraseña",
        validators=[
            DataRequired(),
            EqualTo("password", message="Las contraseñas no coinciden."),
        ],
    )
    submit = SubmitField("Crear cuenta")

    def validate_dni(self, field):
        dni = field.data.strip()

        if not re.fullmatch(r"[0-9]{8}[A-Z]", dni):
            raise ValidationError("Escribe ocho dígitos y una letra mayúscula.")

        if DNI_LETTERS[int(dni[:8]) % 23] != dni[8]:
            raise ValidationError("La letra del DNI no es correcta.")

class LoginForm(FlaskForm):
    class Meta:
        locales = ["es"]

    email = EmailField("Correo electrónico", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    remember = BooleanField("Recordarme")
    submit = SubmitField("Entrar")


