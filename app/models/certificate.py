import uuid
from datetime import datetime

from app.extensions import db


class Certificate(db.Model):
    __tablename__ = "certificates"

    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey("enrollments.id"), unique=True, nullable=False)
    number = db.Column(db.String(50), unique=True, nullable=False, default=lambda: str(uuid.uuid4())[:8].upper())
    issued_on = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    expires_on = db.Column(db.Date, nullable=True)
    file_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Certificate {self.number!r}>"
