from flask import Blueprint

from app.controllers.trainings_controller import TrainingsController
from app.guards.auth import login_required, role_required
from app.utils.enums import UserRole

trainings_bp = Blueprint("trainings", __name__)

_admin_coord = role_required(UserRole.ADMIN, UserRole.COORDINATOR)

trainings_bp.add_url_rule("/", "list", view_func=login_required(TrainingsController.list_page))
trainings_bp.add_url_rule("/form", "form", view_func=_admin_coord(TrainingsController.form_page))
trainings_bp.add_url_rule("/add", "add", view_func=_admin_coord(TrainingsController.create), methods=["POST"])
trainings_bp.add_url_rule("/<int:id>/detail", "detail", view_func=login_required(TrainingsController.detail))
trainings_bp.add_url_rule("/delete/<int:id>", "delete", view_func=_admin_coord(TrainingsController.delete), methods=["POST"])
