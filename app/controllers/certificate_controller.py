import os

from flask import abort, flash, redirect, render_template, send_file, url_for

from app.extensions import db
from app.models.enrollment import Enrollment
from app.models.class_group import ClassGroup
from app.repositories.assessment_repository import AssessmentRepository
from app.repositories.training_repository import TrainingRepository
from app.services.assessment_service import PASSING_GRADE
from app.services.certificate_service import CertificateService
from app.services.email_service import EmailService


class CertificateController:

    @staticmethod
    def admin_list(training_id: int):
        training = TrainingRepository.find_by_id_or_404(training_id)
        enrollments = (
            Enrollment.query
            .join(ClassGroup, Enrollment.class_group_id == ClassGroup.id)
            .filter(ClassGroup.training_id == training_id)
            .all()
        )
        assessments = AssessmentRepository.find_by_training(training_id)

        def best_grade(enrollment):
            grades = [
                AssessmentRepository.find_grade(enrollment.id, a.id)
                for a in assessments
            ]
            valid = [g.grade for g in grades if g and g.grade is not None]
            return float(max(valid)) if valid else None

        rows = [
            {
                "enrollment": e,
                "student": e.student,
                "grade": best_grade(e),
                "cert": e.certificate,
            }
            for e in enrollments
        ]

        return render_template(
            "pages/certificates/admin_list.html",
            training=training,
            rows=rows,
            passing_grade=PASSING_GRADE,
        )

    @staticmethod
    def issue(enrollment_id: int):
        enrollment = db.get_or_404(Enrollment, enrollment_id)
        try:
            cert = CertificateService.issue(enrollment)
            flash(f"Certificado {cert.number} emitido com sucesso.", "success")
        except Exception as e:
            flash(f"Erro ao gerar certificado: {e}", "danger")
        return redirect(url_for(
            "certificates.admin_list",
            training_id=enrollment.class_group.training_id,
        ))

    @staticmethod
    def send_email(enrollment_id: int):
        enrollment = db.get_or_404(Enrollment, enrollment_id)
        cert = enrollment.certificate
        if not cert:
            flash("Emita o certificado antes de enviar.", "warning")
            return redirect(url_for(
                "certificates.admin_list",
                training_id=enrollment.class_group.training_id,
            ))
        try:
            EmailService.send_certificate(enrollment, cert)
            flash(f"Certificado enviado para {enrollment.student.email}.", "success")
        except Exception as e:
            flash(f"Erro ao enviar e-mail: {e}", "danger")
        return redirect(url_for(
            "certificates.admin_list",
            training_id=enrollment.class_group.training_id,
        ))

    @staticmethod
    def download(enrollment_id: int):
        enrollment = db.get_or_404(Enrollment, enrollment_id)
        cert = enrollment.certificate
        if not cert:
            abort(404)
        path = CertificateService.pdf_path(cert)
        if not path or not os.path.exists(path):
            abort(404)
        return send_file(
            path,
            mimetype="application/pdf",
            as_attachment=False,
            download_name=f"Certificado_{cert.number}.pdf",
        )
