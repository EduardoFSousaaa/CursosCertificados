from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

from app.utils.enums import Shift

_SHIFT_CHOICES = [("", "Sem preferência")] + [
    (s.value, s.label) for s in Shift
]


class EnrollmentRequestForm(FlaskForm):
    name = StringField("Nome completo", validators=[
        DataRequired(message="Informe seu nome completo."),
        Length(max=120),
    ])
    badge_number = StringField("Matrícula", validators=[
        DataRequired(message="A matrícula é obrigatória."),
        Length(max=30),
    ])
    sector = StringField("Setor", validators=[
        DataRequired(message="O setor é obrigatório."),
        Length(max=100),
    ])
    email = StringField("E-mail", validators=[
        DataRequired(message="O e-mail é obrigatório."),
        Email(message="Informe um e-mail válido."),
    ])
    password = PasswordField("Senha de acesso", validators=[
        DataRequired(message="Defina uma senha de acesso."),
        Length(min=6, max=128, message="A senha deve ter ao menos 6 caracteres."),
    ])
    confirm_password = PasswordField("Confirme a senha", validators=[
        DataRequired(message="Confirme sua senha."),
        EqualTo("password", message="As senhas não coincidem."),
    ])
    preferred_shift = SelectField("Turno preferido", choices=_SHIFT_CHOICES, validators=[Optional()])
