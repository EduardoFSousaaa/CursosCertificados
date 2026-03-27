import random   
from flask import Blueprint, render_template

home_Routes = Blueprint('home', __name__, template_folder="templates", root_path=f"C:\\Users\\eduar\\Desktop\\pythonVStudio\\CursosCertificados\\app")
@home_Routes.route('/')
def home():
    titulo = "gestao de ussuarios"
    usuarios =[
        {"nome":"guilherme","membro_ativo":True},
        {"nome":"maria","membro_ativo":False},
        {"nome":"joao","membro_ativo":True },
    ]
    return render_template('index.html',titulo=titulo,usuarios=usuarios)