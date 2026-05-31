from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, SelectField, StringField
from wtforms.validators import Length, NumberRange, Optional

from app.utils.enums import Shift

_SHIFT_CHOICES = [(s.value, s.label) for s in Shift]


class ClassGroupForm(FlaskForm):
    name = StringField("Nome da turma", validators=[
        Length(min=1, max=50, message="O nome da turma é obrigatório.")
    ])
    shift = SelectField("Turno", choices=_SHIFT_CHOICES)
    capacity = IntegerField(
        "Vagas (deixe vazio para ilimitado)",
        validators=[Optional(), NumberRange(min=1, message="A capacidade deve ser ao menos 1.")],
    )
    starts_on = DateField("Data início", validators=[Optional()])
    ends_on = DateField("Data término", validators=[Optional()])
