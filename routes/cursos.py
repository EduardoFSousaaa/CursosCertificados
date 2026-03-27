import random  
import ntplib
from datetime import datetime
from flask import Flask ,Blueprint, render_template ,redirect,request
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app) # Objeto db

Cursos_Routes = Blueprint('Cursos', __name__,template_folder="templates",root_path=f"C:\\Users\\eduar\\Desktop\\pythonVStudio\\CursosCertificados\\app")

@Cursos_Routes.route('/source_route', methods=['POST'])
#problema ao enviar formulario tendo de passar os dados do formulario com redirect
def source_function():
    #if request.method == 'POST':
        # Obtém dados de formulário (form data)
        #iTamanhoCampoXeY = request.form.get('TamanhoCampoInput')
        #numeroMinas = request.form.get('NumeroMinasInput')
        #data= {"TamanhoCampoInput" : iTamanhoCampoXeY,
        #      "NumeroMinasInput" : numeroMinas}
    return redirect('/Cursos',code=307)

@Cursos_Routes.route('/',methods=['GET', 'POST'])
def Cursos():
    cursos = Cursos.query.all()
    return render_template('index.html', cursos=cursos)

@Cursos_Routes.route('/',methods=['POST'])
def NovoCurso():
    ano = get_year_from_internet()
    dataInicio = datetime(ano -2, 1, 1)
    dataFim = datetime(ano +1, 12, 31)

    titulo = request.form.get("titulo")
    dataCurso = request.form.get("dataCurso")
    local = request.form.get("local")
    situacao = request.form.get("situacao")

    if titulo != '' and  situacao != "" and \
      dataCurso >= dataInicio and dataCurso <= dataFim:
        p = Cursos(titulo=titulo, dataCurso=dataCurso, local=local,situacao=situacao)
        db.session.add(p)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')

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
