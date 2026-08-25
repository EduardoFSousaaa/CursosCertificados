from flask import Blueprint

from app.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)

auth_bp.add_url_rule("/login", "login", view_func=AuthController.login, methods=["GET", "POST"])
auth_bp.add_url_rule("/logout", "logout", view_func=AuthController.logout)
