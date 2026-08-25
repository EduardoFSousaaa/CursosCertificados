import click
from flask import Flask
from flask.cli import with_appcontext

from app.extensions import db
from app.models.user import User
from app.utils.enums import UserRole


def _create_user(name: str, email: str, badge: str, password: str, role: UserRole) -> User:
    if User.query.filter_by(email=email).first():
        return None
    user = User(name=name, email=email, badge_number=badge, role=role)
    user.set_password(password)
    return user


def run_seed():
    users = [
        _create_user("Admin Sistema", "admin@cursos.com", "ADM001", "admin123", UserRole.ADMIN),
        _create_user("Coordenadora Silva", "coordenadora@cursos.com", "COORD001", "coord123", UserRole.COORDINATOR),
        _create_user("Instrutor Santos", "instrutor@cursos.com", "INST001", "inst123", UserRole.INSTRUCTOR),
        _create_user("Aluno Oliveira", "aluno1@cursos.com", "ALU001", "aluno123", UserRole.STUDENT),
        _create_user("Aluna Ferreira", "aluno2@cursos.com", "ALU002", "aluno123", UserRole.STUDENT),
    ]
    created = [u for u in users if u is not None]
    if created:
        db.session.add_all(created)
        db.session.commit()
        click.echo(f"Seed concluído: {len(created)} usuário(s) criado(s).")
    else:
        click.echo("Seed ignorado: todos os usuários já existem.")


def register_seed_command(app: Flask):
    @app.cli.command("seed")
    @with_appcontext
    def seed_command():
        """Popula o banco com usuários base para testes."""
        run_seed()
