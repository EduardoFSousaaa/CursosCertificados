from flask import Flask, url_for,render_template , request, redirect
from flask_sqlalchemy import SQLAlchemy
from routes.home import home_Routes
from routes.cursos import Cursos_Routes
from sqlalchemy import create_engine
from models import Cursos,AlunosCursos
app = Flask(__name__,template_folder="templates",root_path=f"C:\\Users\\eduar\\Desktop\\pythonVStudio\\CursosCertificados",instance_relative_config=True)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids a warning

# Create SQLAlchemy instance
db = SQLAlchemy(app)
# Run the app and create database

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
