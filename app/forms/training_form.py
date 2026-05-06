from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class TrainingForm(FlaskForm):
    title = StringField(
        "Título",
        validators=[DataRequired(message="O título é obrigatório."), Length(max=200)],
    )
    starts_on = DateField(
        "Data de Início",
        validators=[Optional()],
        format="%Y-%m-%d",
    )
    ends_on = DateField(
        "Data de Término",
        validators=[Optional()],
        format="%Y-%m-%d",
    )
    duration_minutes = IntegerField(
        "Carga Horária (minutos)",
        validators=[Optional(), NumberRange(min=1)],
    )
    location = StringField("Local / Sala", validators=[Optional(), Length(max=200)])
    address = StringField("Endereço", validators=[Optional(), Length(max=300)])
    online_form_url = StringField("Link do Formulário Online", validators=[Optional(), Length(max=500)])
    description = TextAreaField("Conteúdo Programático", validators=[Optional()])
    clinical_skills = TextAreaField("Competências Clínicas", validators=[Optional()])
    required_materials = TextAreaField("Materiais Necessários", validators=[Optional()])
    prerequisites = TextAreaField("Pré-requisitos", validators=[Optional()])
    status = SelectField(
        "Situação",
        choices=[
            ("draft", "Rascunho"),
            ("active", "Ativo"),
            ("in_progress", "Em Andamento"),
            ("completed", "Encerrado"),
            ("cancelled", "Cancelado"),
        ],
        default="draft",
    )
