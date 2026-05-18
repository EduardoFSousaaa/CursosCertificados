from flask import flash, redirect, render_template, url_for
from sqlalchemy import true

from app.controllers.googleController import CredenciaisGoogle
from app.exceptions.app_errors import NotFoundError
from app.forms.training_form import TrainingForm
from app.services.training_service import TrainingService
from app.models.training import Training


class TrainingsController:
    @staticmethod
    def list_page():
        trainings = TrainingService.list_all()
        return render_template("pages/trainings/list.html", trainings=trainings)

    @staticmethod
    def form_page():
        return render_template("pages/trainings/form.html", form=TrainingForm())

    @staticmethod
    def create():
        form = TrainingForm()
        if form.validate_on_submit():
            TrainingService.create(form)
            CreateGoogleFormsTraining(form.idTraining.data)  # Chama a função para criar o formulário no Google Forms:
            flash("Treinamento cadastrado com sucesso!", "success")
        else:
            for field_name, errors in form.errors.items():
                label = getattr(form, field_name).label.text
                for error in errors:
                    flash(f"{label}: {error}", "danger")
        return redirect(url_for("trainings.list"))

    @staticmethod
    def detail(id: int):
        training = TrainingService.get_by_id(id)
        return render_template("pages/trainings/detail.html", training=training)

    @staticmethod
    def delete(id: int):
        try:
            TrainingService.remove(id)
            flash("Treinamento removido.", "warning")
        except NotFoundError:
            flash("Treinamento não encontrado.", "danger")
        return redirect(url_for("trainings.list"))
@staticmethod
def CreateGoogleFormsTraining(id: id):
    from app.controllers.googleController import CredenciaisGoogle

    print("Iniciando processo...")
    forms_service, drive_service = CredenciaisGoogle()
    print("Autenticação válida detectada com sucesso!")
    training = TrainingService.get_by_id(id)
    if training is None:
        return resposta_erro_customizada(id)
    
    # 1. Cria o formulário inicial (Salvo automaticamente no Drive)
    titulo_form = {"info": {"title": training.title,
                             "description": training.description}}
    form = forms_service.forms().create(body=titulo_form).execute()
    # 2. Configura o formulário para coletar e-mails automaticamente
    form.setCollectEmail(true)
    form_id = form['formId']
    
    # 2. Define as perguntas que serão adicionadas
    requisicao_perguntas = {
        TrainingForm.cabecalho_Formulario(training), 
        TrainingForm.perguntas_Funcionarios()
    }
    
    # 3. Envia as perguntas para o formulário
    forms_service.forms().batchUpdate(formId=form_id, body=requisicao_perguntas).execute()
    
    # 4. Pega o link público para incorporar no seu site web
    arquivo_drive = drive_service.files().get(fileId=form_id, fields='webViewLink').execute()
    
    print(f"Formulário estruturado com sucesso!")
    print(f"ID do Formulário: {form_id}")
    print(f"Link para responder: {arquivo_drive['webViewLink']}")
    
    @staticmethod
    def cabecalho_Formulario(training: Training):
        Cabecalho = [{
                "updateFormInfo": {
                    "info": infoCurso(training),
                    "updateMask": infoCurso(training).keys()
                }
            }]
        return Cabecalho

    @staticmethod
    def perguntas_Funcionarios():
        # Bloco da Sessão 1
        sessao_1 = [
            {"createItem": {"item": {"title": "Identificação", "pageBreakItem": {}}, "location": {"index": 0}}},
            {"createItem": {"item": {"title": "Qual o seu nome?", "questionItem": {"question": {"required": True, "textQuestion": {}}}}, "location": {"index": 1}}},
            {"createItem": {"item": {"title": "Qual sua Matrícula?", "questionItem": {"question": {"required": True, "textQuestion": {}}}}, "location": {"index": 2}}},
            {"createItem": {"item": {"title": "Qual seu Setor ?", "questionItem": {"question": {"required": True, "textQuestion": {}}}}, "location": {"index": 3}}}]

        # Bloco da Sessão 2
        sessao_2 = [
            {"createItem": {"item": {"title": "Contato", "pageBreakItem": {}}, "location": {"index": 4}}},
            {"createItem": {"item": {"title": "Qual seu E-mail?", "questionItem": {"question": {"required": True, "textQuestion": {}}}}, "location": {"index": 5}}},
            {"createItem": {"item": {"title": "Qual seu Telefone?", "questionItem": {"question": {"required": True, "textQuestion": {}}}}, "location": {"index": 6}}}
        ]

        # Une os blocos em uma única lista de requests
        return sessao_1 + sessao_2
    
    @staticmethod
    def resposta_erro_customizada(id_treino):
        return {
        "status": "erro",
        "mensagem": f"O treinamento com ID {id_treino} não existe no sistema."
    }

    @staticmethod
    def infoCurso(training: Training):
        #Arrumar itens do Cabecalho do google forms
        return
        {
            "title": training.title, 
            "description": training.description,
            "turnos": training.turnos,
            "lugar": training.locals,
            "Duração": training.duration_minutes,
        }