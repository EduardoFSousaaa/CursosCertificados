from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, TextAreaField
from wtforms.validators import Length, Optional

from app.utils.enums import AssessmentType

_TYPE_CHOICES = [
    (AssessmentType.TECHNICAL_TEST.value, "Prova técnica"),
    (AssessmentType.QUESTIONNAIRE.value, "Questionário"),
    (AssessmentType.PRACTICAL.value, "Avaliação prática"),
]


class AssessmentForm(FlaskForm):
    title = StringField("Título", validators=[
        Length(min=3, max=200, message="O título deve ter ao menos 3 caracteres.")
    ])
    description = TextAreaField("Descrição", validators=[Optional(), Length(max=1000)])
    type = SelectField("Tipo", choices=_TYPE_CHOICES)
    applied_on = DateField("Data de aplicação", validators=[Optional()])
