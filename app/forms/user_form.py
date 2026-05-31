from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField
from wtforms.validators import Email, Length, Optional

from app.utils.enums import UserRole

_ROLE_CHOICES = [
    (UserRole.ADMIN.value,       "Administrador"),
    (UserRole.COORDINATOR.value, "Coordenador"),
    (UserRole.INSTRUCTOR.value,  "Instrutor"),
    (UserRole.STUDENT.value,     "Funcionário"),
]


class UserCreateForm(FlaskForm):
    name         = StringField("Nome completo",  validators=[
        Length(min=3, max=120, message="O nome deve ter ao menos 3 caracteres.")
    ])
    email        = StringField("E-mail",         validators=[
        Email(message="Informe um e-mail válido.")
    ])
    badge_number = StringField("Matrícula",      validators=[
        Length(min=1, max=30, message="A matrícula é obrigatória.")
    ])
    role         = SelectField("Papel",          choices=_ROLE_CHOICES)
    location     = StringField("Setor",          validators=[Optional(), Length(max=200)])
    password     = PasswordField("Senha",        validators=[
        Length(min=6, max=128, message="A senha deve ter ao menos 6 caracteres.")
    ])
