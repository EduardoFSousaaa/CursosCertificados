import uuid

from app.extensions import db
from app.models.training import Training


class TrainingRepository:
    @staticmethod
    def find_all() -> list[Training]:
        return Training.query.order_by(Training.starts_on.desc()).all()

    @staticmethod
    def find_by_id(id: int) -> Training | None:
        return db.session.get(Training, id)

    @staticmethod
    def find_by_id_or_404(id: int) -> Training:
        return db.get_or_404(Training, id)

    @staticmethod
    def find_by_token_or_404(token: str) -> Training:
        return Training.query.filter_by(enrollment_token=token).first_or_404()

    @staticmethod
    def ensure_token(training: Training) -> str:
        """Gera token para treinamentos criados antes da feature existir."""
        if not training.enrollment_token:
            training.enrollment_token = str(uuid.uuid4())
            db.session.commit()
        return training.enrollment_token

    @staticmethod
    def save(training: Training) -> Training:
        db.session.add(training)
        db.session.commit()
        return training

    @staticmethod
    def delete(training: Training) -> None:
        db.session.delete(training)
        db.session.commit()
