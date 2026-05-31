import uuid
from datetime import datetime

from app.extensions import db
from app.utils.enums import TrainingStatus


class Training(db.Model):
    __tablename__ = "trainings"

    id = db.Column(db.Integer, primary_key=True)
    enrollment_token = db.Column(
        db.String(36), unique=True, nullable=True,
        default=lambda: str(uuid.uuid4()),
    )
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    clinical_skills = db.Column(db.Text, nullable=True)
    required_materials = db.Column(db.Text, nullable=True)
    prerequisites = db.Column(db.Text, nullable=True)
    duration_minutes = db.Column(db.Integer, nullable=True)
    starts_on = db.Column(db.Date, nullable=True)
    ends_on = db.Column(db.Date, nullable=True)
    location = db.Column(db.String(200), nullable=True)
    address = db.Column(db.String(300), nullable=True)
    online_form_url = db.Column(db.String(500), nullable=True)
    status = db.Column(
        db.Enum(TrainingStatus, native_enum=False, length=20),
        nullable=False,
        default=TrainingStatus.DRAFT,
    )
    instructor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    class_groups = db.relationship("ClassGroup", backref="training", lazy="select", cascade="all, delete-orphan")
    assessments = db.relationship("Assessment", backref="training", lazy="select", cascade="all, delete-orphan")
    documents = db.relationship("Document", backref="training", lazy="select")

    @property
    def total_enrolled(self) -> int:
        return sum(g.total_enrolled for g in self.class_groups)

    @property
    def duration_formatted(self) -> str:
        if not self.duration_minutes:
            return "—"
        hours, minutes = divmod(self.duration_minutes, 60)
        return f"{hours}h{f'{minutes:02d}min' if minutes else ''}"

    def __repr__(self) -> str:
        return f"<Training {self.title!r}>"
