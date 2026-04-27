import random
import sys   
from flask import Blueprint, render_template
from pathlib import Path

caminho_do_arquivo = Path(__file__).resolve() 
root_path = caminho_do_arquivo.parent.parent
sys.path.append(str(root_path))
home_Routes = Blueprint('home', __name__, template_folder="templates", root_path=root_path)

@home_Routes.route('/')
def home():
    titulo = "gestao de ussuarios"
    usuarios =[
        {"nome":"guilherme","membro_ativo":True},
        {"nome":"maria","membro_ativo":False},
        {"nome":"joao","membro_ativo":True },
    ]
    return render_template('index.html',titulo=titulo,usuarios=usuarios)