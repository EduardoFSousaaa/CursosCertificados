from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

from app.extensions import db
from app.utils.enums import UserRole


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    badge_number = db.Column(db.String(30), unique=True, nullable=False, index=True)
    crm_number = db.Column(db.String(30), nullable=True)
    role = db.Column(
        db.Enum(UserRole, native_enum=False, length=20),
        nullable=False,
        default=UserRole.STUDENT,
    )
    avatar_url = db.Column(db.String(500), nullable=True)
    location = db.Column(db.String(200), nullable=True)
    started_at = db.Column(db.Date, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    trainings_as_instructor = db.relationship(
        "Training",
        foreign_keys="Training.instructor_id",
        backref=db.backref("instructor", lazy="select"),
        lazy="select",
    )
    enrollments = db.relationship(
        "Enrollment",
        foreign_keys="Enrollment.student_id",
        backref=db.backref("student", lazy="select"),
        lazy="select",
        cascade="all, delete-orphan",
    )
    uploaded_documents = db.relationship(
        "Document",
        foreign_keys="Document.uploader_id",
        backref=db.backref("uploader", lazy="select"),
        lazy="select",
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self) -> bool:
        return self.role in (UserRole.ADMIN, UserRole.COORDINATOR)

    @property
    def is_instructor(self) -> bool:
        return self.role == UserRole.INSTRUCTOR

    def __repr__(self) -> str:
        return f"<User {self.name!r} [{self.badge_number}]>"
