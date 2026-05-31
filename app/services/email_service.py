import os

from flask import render_template
from flask_mail import Message

from app.extensions import mail
from app.models.certificate import Certificate
from app.models.enrollment import Enrollment
from app.models.training import Training
from app.models.user import User
from app.services.certificate_service import CertificateService


class EmailService:
    @staticmethod
    def send_certificate(enrollment: Enrollment, cert: Certificate) -> None:
        student = enrollment.student
        training = enrollment.class_group.training

        body_html = render_template(
            "emails/certificate_email.html",
            student=student,
            training=training,
            cert=cert,
        )

        msg = Message(
            subject=f"Certificado de Conclusão — {training.title}",
            recipients=[student.email],
            html=body_html,
        )

        pdf_path = CertificateService.pdf_path(cert)
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                msg.attach(
                    filename=f"Certificado_{cert.number}.pdf",
                    content_type="application/pdf",
                    data=f.read(),
                )

        mail.send(msg)

    @staticmethod
    def send_welcome(user: User, plain_password: str, training: Training) -> None:
        body_html = render_template(
            "emails/welcome_email.html",
            user=user,
            password=plain_password,
            training=training,
        )
        msg = Message(
            subject="Sua inscrição foi aprovada — acesso ao sistema",
            recipients=[user.email],
            html=body_html,
        )
        mail.send(msg)
