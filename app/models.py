from __main__ import db
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
class Cursos(db.Model):
    __tablename__ = "cursos"
    idCurso = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), unique=False, nullable=False)
    dataCurso = db.Column(db.Date,nullable=False)
    local = db.Column(db.String(50), unique=False, nullable=True)
    situacao = db.Column(db.String(40), unique=False, nullable=False)
    turno = db.Column(db.Integer, unique=False, nullable=True)
    turma = db.Column(db.String(20), unique=False, nullable=True)
    horariosAulas = db.Column(db.String(250), unique=False, nullable=True)
    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"Titulo : {self.titulo}, Data do Curso: {self.DataCurso},Local: {self.local},Situação :{self.situacao}"

class AlunosCursos(db.Model):
    __tablename__ = "alunosCursos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=False, nullable=False)
    matricula = db.Column(db.String(10), unique=True, nullable=False)
    dataInscricao = db.Column(db.Date,nullable=False)
    situacao = db.Column(db.String(40), unique=False, nullable=False)
    Curso = db.Column(db.Integer, ForeignKey("cursos.idCurso"), nullable=False)
    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"Aluno : {self.nome},matricula: {self.matricula}, Data da Inscriçao: {self.dataInscricao},Curso Matriculado:{self.Curso},Situação :{self.situacao}"