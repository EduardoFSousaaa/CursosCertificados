import os
from datetime import date

from flask import current_app, render_template

from app.extensions import db
from app.models.certificate import Certificate
from app.models.enrollment import Enrollment

_CERT_DIR = os.path.join("instance", "certificates")


def _cert_dir() -> str:
    path = os.path.join(current_app.root_path, "..", _CERT_DIR)
    os.makedirs(path, exist_ok=True)
    return os.path.abspath(path)


class CertificateService:
    @staticmethod
    def issue(enrollment: Enrollment) -> Certificate:
        """Generate PDF and persist Certificate record. Idempotent — returns existing if already issued."""
        if enrollment.certificate:
            return enrollment.certificate

        cert = Certificate(
            enrollment_id=enrollment.id,
            issued_on=date.today(),
        )
        db.session.add(cert)
        db.session.flush()

        filename = f"cert_{cert.number}.pdf"
        filepath = os.path.join(_cert_dir(), filename)

        html_string = render_template(
            "pages/certificates/certificate.html",
            enrollment=enrollment,
            student=enrollment.student,
            training=enrollment.class_group.training,
            cert=cert,
        )
        from weasyprint import HTML  # lazy import — GTK só disponível no Docker/Linux
        HTML(string=html_string, base_url=current_app.root_path).write_pdf(filepath)

        cert.file_url = filename
        db.session.commit()
        return cert

    @staticmethod
    def pdf_path(cert: Certificate) -> str | None:
        if not cert.file_url:
            return None
        return os.path.join(_cert_dir(), cert.file_url)

    @staticmethod
    def revoke(cert: Certificate) -> None:
        path = CertificateService.pdf_path(cert)
        if path and os.path.exists(path):
            os.remove(path)
        db.session.delete(cert)
        db.session.commit()
