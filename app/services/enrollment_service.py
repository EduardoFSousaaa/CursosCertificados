from datetime import datetime

from flask_login import current_user

from app.exceptions.app_errors import NotFoundError
from app.extensions import db
from app.forms.enrollment_request_form import EnrollmentRequestForm
from app.models.class_group import ClassGroup
from app.models.enrollment import Enrollment
from app.models.enrollment_request import EnrollmentRequest
from app.models.training import Training
from app.models.user import User
from app.repositories.enrollment_request_repository import EnrollmentRequestRepository
from app.utils.enums import EnrollmentRequestStatus, EnrollmentStatus, Shift, UserRole


class EnrollmentService:
    @staticmethod
    def submit_request(training: Training, form: EnrollmentRequestForm) -> EnrollmentRequest:
        from werkzeug.security import generate_password_hash
        preferred_shift = Shift(form.preferred_shift.data) if form.preferred_shift.data else None
        req = EnrollmentRequest(
            training_id=training.id,
            name=form.name.data.strip(),
            email=form.email.data.strip().lower(),
            badge_number=form.badge_number.data.strip(),
            sector=form.sector.data.strip(),
            preferred_shift=preferred_shift,
            password_hash=generate_password_hash(form.password.data),
        )
        return EnrollmentRequestRepository.save(req)

    @staticmethod
    def approve(req: EnrollmentRequest, class_group_id: int) -> Enrollment:
        class_group = db.session.get(ClassGroup, class_group_id)
        if class_group is None or class_group.training_id != req.training_id:
            raise NotFoundError("Turma não encontrada para este treinamento.")

        user = User.query.filter_by(badge_number=req.badge_number).first()
        if user is None:
            email_conflict = User.query.filter_by(email=req.email).first()
            if email_conflict:
                raise ValueError(
                    f"O e-mail '{req.email}' já está cadastrado para outro usuário "
                    f"(matrícula {email_conflict.badge_number}). "
                    "Corrija o e-mail na inscrição ou vincule à matrícula existente."
                )
            user = User(
                name=req.name,
                email=req.email,
                badge_number=req.badge_number,
                location=req.sector,
                role=UserRole.STUDENT,
                password_hash=req.password_hash,
            )
            db.session.add(user)
            db.session.flush()

        enrollment = Enrollment.query.filter_by(
            student_id=user.id,
            class_group_id=class_group.id,
        ).first()
        if enrollment is None:
            enrollment = Enrollment(
                student=user,
                class_group=class_group,
                status=EnrollmentStatus.CONFIRMED,
            )
            db.session.add(enrollment)
        else:
            enrollment.status = EnrollmentStatus.CONFIRMED

        req.status = EnrollmentRequestStatus.APPROVED
        req.reviewed_by_id = current_user.id
        req.reviewed_at = datetime.utcnow()
        req.enrollment = enrollment

        db.session.commit()
        return enrollment

    @staticmethod
    def reject(req: EnrollmentRequest, notes: str = "") -> None:
        req.status = EnrollmentRequestStatus.REJECTED
        req.reviewed_by_id = current_user.id
        req.reviewed_at = datetime.utcnow()
        req.notes = notes
        db.session.commit()
