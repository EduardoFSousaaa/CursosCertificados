from urllib.parse import urljoin, urlparse

from flask import flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user

from app.forms.login_form import LoginForm
from app.models.user import User


def _is_safe_redirect(target: str) -> bool:
    ref = urlparse(request.host_url)
    test = urlparse(urljoin(request.host_url, target))
    return test.scheme in ("http", "https") and ref.netloc == test.netloc


class AuthController:
    @staticmethod
    def login():
        from flask_login import current_user
        if current_user.is_authenticated:
            return redirect(url_for("trainings.list"))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data.lower().strip()).first()
            if not user or not user.check_password(form.password.data):
                flash("Credenciais invalidas.", "danger")
            elif not user.is_active:
                flash("Usuario desativado.", "danger")
            else:
                login_user(user, remember=form.remember.data)
                next_url = request.args.get("next")
                if not next_url or not _is_safe_redirect(next_url):
                    next_url = url_for("trainings.list")
                return redirect(next_url)
        return render_template("pages/auth/login.html", form=form)

    @staticmethod
    def logout():
        logout_user()
        flash("Voce saiu do sistema.", "info")
        return redirect(url_for("auth.login"))
