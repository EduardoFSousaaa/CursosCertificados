from datetime import date

from app.extensions import db
from app.models.enrollment import Attendance, Enrollment


class AttendanceRepository:
    @staticmethod
    def find_by_group_and_date(class_group_id: int, class_date: date) -> list[Attendance]:
        return (
            Attendance.query
            .join(Enrollment)
            .filter(
                Enrollment.class_group_id == class_group_id,
                Attendance.class_date == class_date,
            )
            .all()
        )

    @staticmethod
    def find_by_enrollment_and_date(enrollment_id: int, class_date: date) -> Attendance | None:
        return Attendance.query.filter_by(
            enrollment_id=enrollment_id,
            class_date=class_date,
        ).first()

    @staticmethod
    def dates_with_records(class_group_id: int) -> list[date]:
        rows = (
            db.session.query(Attendance.class_date)
            .join(Enrollment)
            .filter(Enrollment.class_group_id == class_group_id)
            .distinct()
            .order_by(Attendance.class_date.desc())
            .all()
        )
        return [r.class_date for r in rows]

    @staticmethod
    def save_all(records: list[Attendance]) -> None:
        for r in records:
            db.session.add(r)
        db.session.commit()
