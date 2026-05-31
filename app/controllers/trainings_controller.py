from flask import flash, redirect, render_template, url_for
from flask_login import current_user

from app.exceptions.app_errors import NotFoundError
from app.forms.training_form import TrainingForm
from app.models.enrollment import Enrollment
from app.models.class_group import ClassGroup
from app.models.training import Training
from app.services.training_service import TrainingService


class TrainingsController:
    @staticmethod
    def list_page():
        if current_user.is_admin:
            trainings = TrainingService.list_all()
        elif current_user.is_instructor:
            trainings = (
                Training.query
                .filter_by(instructor_id=current_user.id)
                .order_by(Training.starts_on.desc())
                .all()
            )
        else:
            from app.extensions import db
            trainings = (
                db.session.query(Training)
                .join(ClassGroup, ClassGroup.training_id == Training.id)
                .join(Enrollment, Enrollment.class_group_id == ClassGroup.id)
                .filter(Enrollment.student_id == current_user.id)
                .distinct()
                .order_by(Training.starts_on.desc())
                .all()
            )
        return render_template("pages/trainings/list.html", trainings=trainings)

    @staticmethod
    def form_page():
        form = TrainingForm()
        TrainingsController._set_instructor_choices(form)
        return render_template("pages/trainings/form.html", form=form)

    @staticmethod
    def _set_instructor_choices(form):
        from app.models.user import User
        from app.utils.enums import UserRole
        instructors = User.query.filter_by(role=UserRole.INSTRUCTOR).order_by(User.name).all()
        form.instructor_id.choices = [("", "— Nenhum —")] + [(str(u.id), u.name) for u in instructors]

    @staticmethod
    def create():
        form = TrainingForm()
        TrainingsController._set_instructor_choices(form)
        if form.validate_on_submit():
            TrainingService.create(form)
            flash("Treinamento cadastrado com sucesso!", "success")
        else:
            for field_name, errors in form.errors.items():
                label = getattr(form, field_name).label.text
                for error in errors:
                    flash(f"{label}: {error}", "danger")
        return redirect(url_for("trainings.list"))

    @staticmethod
    def detail(id: int):
        from app.models.assessment import AssessmentGrade
        from app.models.enrollment import Enrollment
        from app.models.class_group import ClassGroup

        training = TrainingService.get_by_id(id)

        assessment_status = []
        if not current_user.is_admin and not current_user.is_instructor:
            enrollment = (
                Enrollment.query
                .join(ClassGroup, Enrollment.class_group_id == ClassGroup.id)
                .filter(
                    ClassGroup.training_id == training.id,
                    Enrollment.student_id == current_user.id,
                )
                .first()
            )
            if enrollment:
                for a in training.assessments:
                    grade = AssessmentGrade.query.filter_by(
                        enrollment_id=enrollment.id,
                        assessment_id=a.id,
                    ).first()
                    assessment_status.append({"assessment": a, "grade": grade})

        return render_template(
            "pages/trainings/detail.html",
            training=training,
            assessment_status=assessment_status,
        )

    @staticmethod
    def delete(id: int):
        try:
            TrainingService.remove(id)
            flash("Treinamento removido.", "warning")
        except NotFoundError:
            flash("Treinamento não encontrado.", "danger")
        return redirect(url_for("trainings.list"))

    @staticmethod
    def set_status(id: int):
        from flask import request
        from app.utils.enums import TrainingStatus
        training = TrainingService.get_by_id(id)
        new_status = request.form.get("status")
        try:
            training.status = TrainingStatus(new_status)
            from app.extensions import db
            db.session.commit()
            flash(f"Status alterado para '{training.status.value}'.", "success")
        except ValueError:
            flash("Status inválido.", "danger")
        return redirect(url_for("trainings.list"))
