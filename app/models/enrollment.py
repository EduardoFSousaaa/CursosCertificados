from datetime import datetime

from app.extensions import db
from app.utils.enums import EnrollmentStatus, FinalConcept


class Enrollment(db.Model):
    __tablename__ = "enrollments"
    __table_args__ = (
        db.UniqueConstraint("student_id", "class_group_id", name="uq_enrollment_student_class_group"),
    )

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    class_group_id = db.Column(db.Integer, db.ForeignKey("class_groups.id"), nullable=False, index=True)
    status = db.Column(
        db.Enum(EnrollmentStatus, native_enum=False, length=20),
        nullable=False,
        default=EnrollmentStatus.PENDING,
    )
    final_grade = db.Column(db.Numeric(5, 2), nullable=True)
    final_concept = db.Column(
        db.Enum(FinalConcept, native_enum=False, length=15),
        nullable=False,
        default=FinalConcept.PENDING,
    )
    attendance_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    notes = db.Column(db.Text, nullable=True)
    enrolled_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    attendances = db.relationship("Attendance", backref="enrollment", lazy="select", cascade="all, delete-orphan")
    assessment_grades = db.relationship("AssessmentGrade", backref="enrollment", lazy="select", cascade="all, delete-orphan")
    answers = db.relationship("StudentAnswer", backref="enrollment", lazy="select", cascade="all, delete-orphan")
    certificate = db.relationship("Certificate", backref="enrollment", uselist=False, cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Enrollment student_id={self.student_id} class_group_id={self.class_group_id}>"


class Attendance(db.Model):
    __tablename__ = "attendances"

    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey("enrollments.id"), nullable=False, index=True)
    class_date = db.Column(db.Date, nullable=False)
    is_present = db.Column(db.Boolean, nullable=False, default=False)
    note = db.Column(db.String(300), nullable=True)
    recorded_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    recorded_by = db.relationship("User", foreign_keys=[recorded_by_id])

    def __repr__(self) -> str:
        return f"<Attendance enrollment_id={self.enrollment_id} date={self.class_date} present={self.is_present}>"
