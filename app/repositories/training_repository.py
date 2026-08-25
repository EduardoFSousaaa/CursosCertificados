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
    def save(training: Training) -> Training:
        db.session.add(training)
        db.session.commit()
        return training

    @staticmethod
    def delete(training: Training) -> None:
        db.session.delete(training)
        db.session.commit()
