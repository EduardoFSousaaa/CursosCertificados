import os

from flask import Flask

from .config import config
from .extensions import cors, csrf, db, login_manager, mail, migrate

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_app(env: str | None = None) -> Flask:
    if env is None:
        env = os.environ.get("FLASK_ENV", "development")

    app = Flask(
        __name__,
        template_folder=os.path.join(_ROOT, "frontend", "templates"),
        static_folder=os.path.join(_ROOT, "frontend", "static"),
    )
    app.config.from_object(config[env])

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    mail.init_app(app)
    cors.init_app(app, resources={})  # CORS disabled globally; configure per-route as needed

    from .security.session import init_login
    init_login(app)

    from .filters.jinja_filters import register_filters
    register_filters(app)

    from .interceptors.request_hooks import register_hooks
    register_hooks(app)

    from .errors.handlers import register_error_handlers
    register_error_handlers(app)

    # Import models so Alembic can detect them during migrations
    from .models import (  # noqa: F401
        Assessment, AssessmentGrade, Certificate, ClassGroup, Document,
        Attendance, Enrollment, EnrollmentRequest, Question, QuestionOption,
        StudentAnswer, Training, User,
    )

    from .routes.home import home_bp
    from .routes.trainings import trainings_bp
    from .routes.auth import auth_bp
    from .routes.enrollments import enrollments_bp
    from .routes.attendance import attendance_bp
    from .routes.assessments import assessments_bp
    from .routes.certificates import certificates_bp
    from .routes.class_groups import class_groups_bp
    from .routes.users import users_bp
    from .routes.reports import reports_bp

    app.register_blueprint(home_bp, url_prefix="/home")
    app.register_blueprint(trainings_bp, url_prefix="/trainings")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(enrollments_bp, url_prefix="/inscricao")
    app.register_blueprint(attendance_bp, url_prefix="/presenca")
    app.register_blueprint(assessments_bp, url_prefix="/provas")
    app.register_blueprint(certificates_bp, url_prefix="/certificados")
    app.register_blueprint(class_groups_bp, url_prefix="/turmas")
    app.register_blueprint(users_bp, url_prefix="/usuarios")
    app.register_blueprint(reports_bp, url_prefix="/relatorios")

    @app.route("/")
    def index():
        from flask import render_template
        return render_template("pages/home/index.html")

    @app.after_request
    def security_headers(response):
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        if not app.debug:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

    return app
