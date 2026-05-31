from app.extensions import db
from app.models.enrollment_request import EnrollmentRequest
from app.utils.enums import EnrollmentRequestStatus


class EnrollmentRequestRepository:
    @staticmethod
    def save(request: EnrollmentRequest) -> EnrollmentRequest:
        db.session.add(request)
        db.session.commit()
        return request

    @staticmethod
    def find_by_id(id: int) -> EnrollmentRequest | None:
        return db.session.get(EnrollmentRequest, id)

    @staticmethod
    def find_by_id_or_404(id: int) -> EnrollmentRequest:
        return db.get_or_404(EnrollmentRequest, id)

    @staticmethod
    def find_pending_by_training(training_id: int) -> list[EnrollmentRequest]:
        return (
            EnrollmentRequest.query
            .filter_by(training_id=training_id, status=EnrollmentRequestStatus.PENDING)
            .order_by(EnrollmentRequest.requested_at.asc())
            .all()
        )

    @staticmethod
    def find_all_by_training(training_id: int) -> list[EnrollmentRequest]:
        return (
            EnrollmentRequest.query
            .filter_by(training_id=training_id)
            .order_by(EnrollmentRequest.requested_at.desc())
            .all()
        )

    @staticmethod
    def already_requested(training_id: int, badge_number: str) -> bool:
        return EnrollmentRequest.query.filter(
            EnrollmentRequest.training_id == training_id,
            EnrollmentRequest.badge_number == badge_number,
            EnrollmentRequest.status != EnrollmentRequestStatus.REJECTED,
        ).first() is not None
