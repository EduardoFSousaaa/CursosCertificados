from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user

from app.exceptions.app_errors import NotFoundError
from app.forms.enrollment_request_form import EnrollmentRequestForm
from app.repositories.enrollment_request_repository import EnrollmentRequestRepository
from app.repositories.training_repository import TrainingRepository
from app.services.enrollment_service import EnrollmentService


class EnrollmentController:
    @staticmethod
    def public_form(token: str):
        training = TrainingRepository.find_by_token_or_404(token)
        form = EnrollmentRequestForm()
        return render_template(
            "pages/enrollments/public_form.html",
            training=training,
            form=form,
            token=token,
        )

    @staticmethod
    def submit(token: str):
        training = TrainingRepository.find_by_token_or_404(token)
        form = EnrollmentRequestForm()

        if not form.validate_on_submit():
            return render_template(
                "pages/enrollments/public_form.html",
                training=training,
                form=form,
                token=token,
            )

        if EnrollmentRequestRepository.already_requested(training.id, form.badge_number.data.strip()):
            return render_template(
                "pages/enrollments/public_form.html",
                training=training,
                form=form,
                token=token,
                duplicate=True,
            )

        EnrollmentService.submit_request(training, form)
        return redirect(url_for("enrollments.success", token=token))

    @staticmethod
    def success(token: str):
        training = TrainingRepository.find_by_token_or_404(token)
        return render_template("pages/enrollments/success.html", training=training)

    @staticmethod
    def admin_list(training_id: int):
        training = TrainingRepository.find_by_id_or_404(training_id)
        if current_user.is_instructor and training.instructor_id != current_user.id:
            abort(403)
        requests = EnrollmentRequestRepository.find_all_by_training(training_id)
        return render_template(
            "pages/enrollments/admin_list.html",
            training=training,
            requests=requests,
        )

    @staticmethod
    def approve(training_id: int, req_id: int):
        req = EnrollmentRequestRepository.find_by_id_or_404(req_id)
        class_group_id = request.form.get("class_group_id", type=int)
        if not class_group_id:
            flash("Selecione uma turma para aprovar a inscrição.", "danger")
            return redirect(url_for("enrollments.admin_list", training_id=training_id))
        try:
            EnrollmentService.approve(req, class_group_id)
            flash("Inscrição aprovada com sucesso.", "success")
        except (NotFoundError, ValueError) as e:
            flash(str(e), "danger")
        return redirect(url_for("enrollments.admin_list", training_id=training_id))

    @staticmethod
    def reject(training_id: int, req_id: int):
        req = EnrollmentRequestRepository.find_by_id_or_404(req_id)
        notes = request.form.get("notes", "")
        EnrollmentService.reject(req, notes)
        flash("Inscrição rejeitada.", "warning")
        return redirect(url_for("enrollments.admin_list", training_id=training_id))
