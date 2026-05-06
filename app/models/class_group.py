from datetime import datetime

from app.extensions import db
from app.utils.enums import Shift


class ClassGroup(db.Model):
    __tablename__ = "class_groups"

    id = db.Column(db.Integer, primary_key=True)
    training_id = db.Column(db.Integer, db.ForeignKey("trainings.id"), nullable=False, index=True)
    name = db.Column(db.String(50), nullable=False)
    shift = db.Column(
        db.Enum(Shift, native_enum=False, length=15),
        nullable=False,
    )
    starts_at = db.Column(db.String(5), nullable=True)
    ends_at = db.Column(db.String(5), nullable=True)
    capacity = db.Column(db.Integer, nullable=True)
    starts_on = db.Column(db.Date, nullable=True)
    ends_on = db.Column(db.Date, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    enrollments = db.relationship("Enrollment", backref="class_group", lazy="select", cascade="all, delete-orphan")

    @property
    def total_enrolled(self) -> int:
        return len(self.enrollments)

    @property
    def available_spots(self) -> int | None:
        if self.capacity is None:
            return None
        return max(0, self.capacity - self.total_enrolled)

    @property
    def shift_label(self) -> str:
        return self.shift.label if self.shift else "—"

    def __repr__(self) -> str:
        return f"<ClassGroup {self.name!r} [{self.shift_label}]>"
