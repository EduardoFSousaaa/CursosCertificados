from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user

from app.extensions import db
from app.forms.class_group_form import ClassGroupForm
from app.models.class_group import ClassGroup
from app.models.enrollment import Enrollment
from app.models.user import User
from app.repositories.class_group_repository import ClassGroupRepository
from app.repositories.training_repository import TrainingRepository
from app.repositories.user_repository import UserRepository
from app.utils.enums import EnrollmentStatus, Shift


class ClassGroupController:

    @staticmethod
    def manage(training_id: int):
        training = TrainingRepository.find_by_id_or_404(training_id)
        form = ClassGroupForm()
        return render_template(
            "pages/class_groups/manage.html",
            training=training,
            form=form,
        )

    @staticmethod
    def create(training_id: int):
        training = TrainingRepository.find_by_id_or_404(training_id)
        form = ClassGroupForm()
        if form.validate_on_submit():
            group = ClassGroup(
                training_id=training.id,
                name=form.name.data.strip(),
                shift=Shift(form.shift.data),
                capacity=form.capacity.data,
                starts_on=form.starts_on.data,
                ends_on=form.ends_on.data,
            )
            ClassGroupRepository.save(group)
            flash(f"Turma '{group.name}' criada.", "success")
        else:
            for field, errors in form.errors.items():
                for e in errors:
                    flash(f"{getattr(form, field).label.text}: {e}", "danger")
        return redirect(url_for("class_groups.manage", training_id=training_id))

    @staticmethod
    def delete(training_id: int, group_id: int):
        group = ClassGroupRepository.find_by_id_or_404(group_id)
        if group.enrollments:
            flash("Não é possível excluir uma turma com alunos inscritos.", "danger")
        else:
            ClassGroupRepository.delete(group)
            flash("Turma removida.", "warning")
        return redirect(url_for("class_groups.manage", training_id=training_id))

    @staticmethod
    def enroll_manual(training_id: int, group_id: int):
        group = ClassGroupRepository.find_by_id_or_404(group_id)
        badge = request.form.get("badge_number", "").strip()

        if not badge:
            flash("Informe a matrícula.", "danger")
            return redirect(url_for("class_groups.manage", training_id=training_id))

        user = UserRepository.find_by_badge(badge)
        if user is None:
            flash(f"Nenhum usuário encontrado com matrícula '{badge}'.", "danger")
            return redirect(url_for("class_groups.manage", training_id=training_id))

        already = Enrollment.query.filter_by(
            student_id=user.id, class_group_id=group.id
        ).first()
        if already:
            flash(f"{user.name} já está inscrito nesta turma.", "warning")
            return redirect(url_for("class_groups.manage", training_id=training_id))

        enrollment = Enrollment(
            student_id=user.id,
            class_group_id=group.id,
            status=EnrollmentStatus.CONFIRMED,
        )
        db.session.add(enrollment)
        db.session.commit()
        flash(f"{user.name} inscrito com sucesso.", "success")
        return redirect(url_for("class_groups.manage", training_id=training_id))
