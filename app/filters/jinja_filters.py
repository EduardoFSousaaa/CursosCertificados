from datetime import date, datetime


def format_date(value: date | datetime | None, fmt: str = "%d/%m/%Y") -> str:
    if value is None:
        return "—"
    return value.strftime(fmt)


def format_duration(minutes: int | None) -> str:
    if not minutes:
        return "—"
    hours, mins = divmod(minutes, 60)
    return f"{hours}h{f'{mins:02d}min' if mins else ''}"


def shift_label(shift) -> str:
    return shift.label if shift else "—"


_TRAINING_STATUS_LABELS = {
    "draft":       "Rascunho",
    "active":      "Ativo",
    "in_progress": "Em andamento",
    "completed":   "Concluído",
    "cancelled":   "Cancelado",
}

_TRAINING_STATUS_COLORS = {
    "draft":       "warning",
    "active":      "success",
    "in_progress": "primary",
    "completed":   "secondary",
    "cancelled":   "danger",
}

_USER_ROLE_LABELS = {
    "admin":       "Administrador",
    "coordinator": "Coordenador",
    "instructor":  "Instrutor",
    "student":     "Funcionário",
}


def training_status_label(status) -> str:
    val = status.value if hasattr(status, "value") else str(status)
    return _TRAINING_STATUS_LABELS.get(val, val)


def training_status_color(status) -> str:
    val = status.value if hasattr(status, "value") else str(status)
    return _TRAINING_STATUS_COLORS.get(val, "secondary")


def user_role_label(role) -> str:
    val = role.value if hasattr(role, "value") else str(role)
    return _USER_ROLE_LABELS.get(val, val.title())


def register_filters(app):
    app.jinja_env.filters["format_date"]            = format_date
    app.jinja_env.filters["format_duration"]        = format_duration
    app.jinja_env.filters["shift_label"]            = shift_label
    app.jinja_env.filters["training_status_label"]  = training_status_label
    app.jinja_env.filters["training_status_color"]  = training_status_color
    app.jinja_env.filters["user_role_label"]        = user_role_label
