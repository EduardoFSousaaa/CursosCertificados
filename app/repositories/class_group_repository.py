from app.extensions import db
from app.models.class_group import ClassGroup


class ClassGroupRepository:
    @staticmethod
    def find_by_id_or_404(id: int) -> ClassGroup:
        return db.get_or_404(ClassGroup, id)

    @staticmethod
    def save(group: ClassGroup) -> ClassGroup:
        db.session.add(group)
        db.session.commit()
        return group

    @staticmethod
    def delete(group: ClassGroup) -> None:
        db.session.delete(group)
        db.session.commit()
