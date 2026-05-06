from app.extensions import db
from app.models.user import User


class UserRepository:
    @staticmethod
    def find_all() -> list[User]:
        return User.query.order_by(User.name).all()

    @staticmethod
    def find_by_id(id: int) -> User | None:
        return db.session.get(User, id)

    @staticmethod
    def find_by_email(email: str) -> User | None:
        return User.query.filter_by(email=email).first()

    @staticmethod
    def find_by_badge(badge_number: str) -> User | None:
        return User.query.filter_by(badge_number=badge_number).first()

    @staticmethod
    def save(user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def delete(user: User) -> None:
        db.session.delete(user)
        db.session.commit()
