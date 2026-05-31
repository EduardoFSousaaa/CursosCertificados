from flask import Blueprint

from app.controllers.assessment_controller import AssessmentController
from app.guards.auth import login_required, role_required
from app.utils.enums import UserRole

assessments_bp = Blueprint("assessments", __name__)

_admin_coord = role_required(UserRole.ADMIN, UserRole.COORDINATOR)
_admin_coord_instructor = role_required(UserRole.ADMIN, UserRole.COORDINATOR, UserRole.INSTRUCTOR)
_any_auth = login_required

# ── Admin ──────────────────────────────────────────────────────────────────
assessments_bp.add_url_rule(
    "/treinamento/<int:training_id>",
    "list_page",
    view_func=_admin_coord(login_required(AssessmentController.list_page)),
    methods=["GET"],
)
assessments_bp.add_url_rule(
    "/treinamento/<int:training_id>/nova",
    "create",
    view_func=_admin_coord(login_required(AssessmentController.create)),
    methods=["POST"],
)
assessments_bp.add_url_rule(
    "/<int:assessment_id>/questoes",
    "questions",
    view_func=_admin_coord(login_required(AssessmentController.questions)),
    methods=["GET"],
)
assessments_bp.add_url_rule(
    "/<int:assessment_id>/questoes/adicionar",
    "add_question",
    view_func=_admin_coord(login_required(AssessmentController.add_question)),
    methods=["POST"],
)
assessments_bp.add_url_rule(
    "/<int:assessment_id>/questoes/<int:question_id>/excluir",
    "delete_question",
    view_func=_admin_coord(login_required(AssessmentController.delete_question)),
    methods=["POST"],
)
assessments_bp.add_url_rule(
    "/<int:assessment_id>/resultados",
    "results",
    view_func=_admin_coord_instructor(login_required(AssessmentController.results)),
    methods=["GET"],
)

# ── Aluno ──────────────────────────────────────────────────────────────────
assessments_bp.add_url_rule(
    "/<int:assessment_id>/responder",
    "take",
    view_func=login_required(AssessmentController.take),
    methods=["GET"],
)
assessments_bp.add_url_rule(
    "/<int:assessment_id>/submeter",
    "submit",
    view_func=login_required(AssessmentController.submit),
    methods=["POST"],
)
assessments_bp.add_url_rule(
    "/<int:assessment_id>/resultado",
    "result",
    view_func=login_required(AssessmentController.result),
    methods=["GET"],
)
