import random
import sys  
import ntplib
from datetime import datetime
from flask import Flask ,Blueprint, render_template ,redirect,request
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from models import Cursos,AlunosCursos

from __main__ import db 

caminho_do_arquivo = Path(__file__).resolve() 
root_path = caminho_do_arquivo.parent.parent
sys.path.append(str(root_path))

Cursos_Routes = Blueprint('cursos', __name__,template_folder="templates",root_path=root_path,url_prefix='/cursos')

@Cursos_Routes.route('/source_route', methods=['POST'])
#problema ao enviar formulario tendo de passar os dados do formulario com redirect
def source_function():
    #if request.method == 'POST':
        # Obtém dados de formulário (form data)
        #iTamanhoCampoXeY = request.form.get('TamanhoCampoInput')
        #numeroMinas = request.form.get('NumeroMinasInput')
        #data= {"TamanhoCampoInput" : iTamanhoCampoXeY,
        #      "NumeroMinasInput" : numeroMinas}
    return redirect('/cursos',code=307)

@Cursos_Routes.route('/cursos',methods=['GET', 'POST'])
def cursos():
    # O objeto 'Cursos' já tem um atributo .query embutido pelo Flask-SQLAlchemy
    lista_cursos = Cursos.query.all() 
    return render_template('cursos.html', cursos=lista_cursos)

@Cursos_Routes.route('/formNovoCurso')
def formulario_curso():
    HorariosAulas =  "Manha: 08:00 até 12:00.\nTarde: 14:00 até 18:00.\nNoite: 19:00 até 22:00."
    return render_template('addCurso.html',HorariosAulas=HorariosAulas)

@Cursos_Routes.route('/add',methods=['POST'])
def NovoCurso():
    ano = get_year_from_internet()
    dataInicio = datetime(ano -2, 1, 1)
    dataFim = datetime(ano +1, 12, 31)
    turnos_selecionados  = request.form.getlist('turnos') 
    titulo = request.form.get("titulo")
    dataCurso = request.form.get("dataCurso")
    local = request.form.get("local")
    situacao = request.form.get("situacao")
    turnos_string = ";".join(turnos_selecionados)
    turma = request.form.get("turma")
    if titulo != '' and  situacao != "" and \
      dataCurso >= dataInicio and dataCurso <= dataFim:
        p = Cursos(titulo=titulo, dataCurso=dataCurso, local=local,turnos = turnos_string, situacao=situacao)
        db.session.add(p)
        db.session.commit()
        return redirect('/cursos')
    else:
        return redirect('/cursos')

@Cursos_Routes.route('/delete/<int:idCurso>',methods=['GET', 'POST'])
def DeletarCurso(idCurso):
    data = Cursos.query.get(idCurso)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')

def get_year_from_internet():
    try:
        c = ntplib.NTPClient()
        # Consulta um servidor NTP público
        response = c.request('pool.ntp.org', version=3)
        # Converte o timestamp para datetime
        date_obj = datetime.fromtimestamp(response.tx_time)
        return date_obj.year
    except:
        # Fallback para o ano local se a internet falhar
        return datetime.now().year
