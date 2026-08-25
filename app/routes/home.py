from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def index():
    titulo = "Gestão de Usuários"
    usuarios = [
        {"nome": "Guilherme", "membro_ativo": True},
        {"nome": "Maria", "membro_ativo": False},
        {"nome": "João", "membro_ativo": True},
    ]
    return render_template("pages/home/index.html", titulo=titulo, usuarios=usuarios)
