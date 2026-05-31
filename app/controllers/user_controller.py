from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user

from app.extensions import db
from app.forms.user_form import UserCreateForm
from app.models.enrollment import Enrollment
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils.enums import UserRole


class UserController:

    @staticmethod
    def own_profile():
        return UserController._profile_page(current_user)

    @staticmethod
    def profile(user_id: int):
        if not current_user.is_admin and current_user.id != user_id:
            abort(403)
        user = db.get_or_404(User, user_id)
        return UserController._profile_page(user)

    @staticmethod
    def _profile_page(user: User):
        enrollments = (
            Enrollment.query
            .filter_by(student_id=user.id)
            .order_by(Enrollment.enrolled_at.desc())
            .all()
        )
        return render_template(
            "pages/users/profile.html",
            subject=user,
            enrollments=enrollments,
        )

    @staticmethod
    def list_users():
        users = UserRepository.find_all()
        form = UserCreateForm()
        return render_template("pages/users/list.html", users=users, form=form)

    @staticmethod
    def create_user():
        form = UserCreateForm()
        if form.validate_on_submit():
            if User.query.filter_by(email=form.email.data.lower().strip()).first():
                flash("Já existe um usuário com este e-mail.", "danger")
                return redirect(url_for("users.list_users"))
            if User.query.filter_by(badge_number=form.badge_number.data.strip()).first():
                flash("Já existe um usuário com esta matrícula.", "danger")
                return redirect(url_for("users.list_users"))
            user = User(
                name=form.name.data.strip(),
                email=form.email.data.lower().strip(),
                badge_number=form.badge_number.data.strip(),
                role=UserRole(form.role.data),
                location=form.location.data.strip() if form.location.data else None,
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash(f"Usuário '{user.name}' criado com sucesso.", "success")
        else:
            for field, errors in form.errors.items():
                for e in errors:
                    flash(f"{getattr(form, field).label.text}: {e}", "danger")
        return redirect(url_for("users.list_users"))
