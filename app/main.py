import sys

from flask import Flask, url_for,render_template , request, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine

from pathlib import Path

caminho_do_arquivo = Path(__file__).resolve() 
root_path = caminho_do_arquivo.parent.parent
sys.path.append(str(root_path))
app = Flask(__name__,template_folder="templates",root_path=root_path,instance_relative_config=True)

# Create SQLAlchemy instance

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids a warning

# Run the app and create database
db = SQLAlchemy(app)

from .routes.home import home_Routes
from .routes.cursos import Cursos_Routes
from models import Cursos,AlunosCursos

if __name__ == '__main__':
    with app.app_context():  # Needed for DB operations
        db.create_all()      # Creates the database and tables

app.register_blueprint(home_Routes,url_prefix='/home')
app.register_blueprint(Cursos_Routes,url_prefix='/cursos')
# rotas
@app.route('/')
def pagina_inicial():
    return "<h1>Pagina inicial</h1>" + f" <a href='{url_for('cursos.cursos')}'> Turmas de treinamento</a>"
@app.route('/sobre')
def pagina_sobre():
    return """
        <p>Pagina sobre exemplo</p>
   """
#execução
app.run(debug=True)
