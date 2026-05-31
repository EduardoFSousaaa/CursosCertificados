from datetime import date

from flask_login import current_user

from app.models.enrollment import Attendance, Enrollment
from app.repositories.attendance_repository import AttendanceRepository


class AttendanceService:
    @staticmethod
    def get_session(class_group_id: int, class_date: date) -> dict[int, Attendance]:
        """Returns {enrollment_id: Attendance} for every enrollment in the group on that date."""
        existing = AttendanceRepository.find_by_group_and_date(class_group_id, class_date)
        return {a.enrollment_id: a for a in existing}

    @staticmethod
    def save(enrollments: list[Enrollment], class_date: date, present_ids: set[int]) -> None:
        """Upserts one Attendance row per enrollment for the given date."""
        existing_map = {
            a.enrollment_id: a
            for a in AttendanceRepository.find_by_group_and_date(
                enrollments[0].class_group_id if enrollments else 0,
                class_date,
            )
        }

        to_save: list[Attendance] = []
        for enrollment in enrollments:
            record = existing_map.get(enrollment.id)
            is_present = enrollment.id in present_ids

            if record is None:
                record = Attendance(
                    enrollment_id=enrollment.id,
                    class_date=class_date,
                    is_present=is_present,
                    recorded_by_id=current_user.id,
                )
            else:
                record.is_present = is_present
                record.recorded_by_id = current_user.id

            to_save.append(record)

        AttendanceRepository.save_all(to_save)
