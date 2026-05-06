from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = EmailField(
        "E-mail Institucional",
        validators=[DataRequired(message="Informe o e-mail."), Email(message="E-mail invalido."), Length(max=150)],
    )
    password = PasswordField(
        "Senha",
        validators=[DataRequired(message="Informe a senha."), Length(min=6, max=128)],
    )
    remember = BooleanField("Manter conectado por 30 dias")
