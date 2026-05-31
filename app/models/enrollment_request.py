from datetime import datetime

from app.extensions import db
from app.utils.enums import EnrollmentRequestStatus, Shift


class EnrollmentRequest(db.Model):
    __tablename__ = "enrollment_requests"

    id = db.Column(db.Integer, primary_key=True)
    training_id = db.Column(db.Integer, db.ForeignKey("trainings.id", ondelete="CASCADE"), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    badge_number = db.Column(db.String(30), nullable=False)
    sector = db.Column(db.String(100), nullable=False)
    preferred_shift = db.Column(
        db.Enum(Shift, native_enum=False, length=15),
        nullable=True,
    )
    status = db.Column(
        db.Enum(EnrollmentRequestStatus, native_enum=False, length=15),
        nullable=False,
        default=EnrollmentRequestStatus.PENDING,
    )
    password_hash = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    requested_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    reviewed_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey("enrollments.id"), nullable=True)

    training = db.relationship("Training", backref=db.backref("enrollment_requests", lazy="dynamic"), passive_deletes=True)
    reviewed_by = db.relationship("User", foreign_keys=[reviewed_by_id])
    enrollment = db.relationship("Enrollment", foreign_keys=[enrollment_id])

    def __repr__(self) -> str:
        return f"<EnrollmentRequest {self.badge_number!r} training_id={self.training_id} status={self.status.value}>"
