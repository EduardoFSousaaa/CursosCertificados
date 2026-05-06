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


def register_filters(app):
    app.jinja_env.filters["format_date"] = format_date
    app.jinja_env.filters["format_duration"] = format_duration
    app.jinja_env.filters["shift_label"] = shift_label
