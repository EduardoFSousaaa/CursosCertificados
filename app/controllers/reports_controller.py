from flask import render_template
from sqlalchemy import func

from app.extensions import db
from app.models.certificate import Certificate
from app.models.class_group import ClassGroup
from app.models.enrollment import Enrollment
from app.models.user import User
from app.utils.enums import FinalConcept


class ReportsController:

    @staticmethod
    def sectors():
        rows = (
            db.session.query(
                func.coalesce(User.location, "Não informado").label("sector"),
                func.count(Enrollment.id).label("total"),
                func.sum(
                    db.case((Enrollment.final_concept == FinalConcept.APPROVED, 1), else_=0)
                ).label("approved"),
            )
            .join(Enrollment, Enrollment.student_id == User.id)
            .group_by(func.coalesce(User.location, "Não informado"))
            .order_by(func.count(Enrollment.id).desc())
            .all()
        )

        cert_by_sector = dict(
            db.session.query(
                func.coalesce(User.location, "Não informado"),
                func.count(Certificate.id),
            )
            .join(Enrollment, Enrollment.student_id == User.id)
            .join(Certificate, Certificate.enrollment_id == Enrollment.id)
            .group_by(func.coalesce(User.location, "Não informado"))
            .all()
        )

        total_enrollments = sum(r.total for r in rows) or 1

        data = [
            {
                "sector": r.sector,
                "total": r.total,
                "approved": int(r.approved or 0),
                "certificates": cert_by_sector.get(r.sector, 0),
                "pct": round((r.total / total_enrollments) * 100),
            }
            for r in rows
        ]

        return render_template("pages/reports/sectors.html", data=data,
                               total_enrollments=total_enrollments)
