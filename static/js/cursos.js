function fechamodal(strModal) {
  const myModalElement = document.getElementById(strModal);
  const myModal = bootstrap.Modal.getInstance(myModalElement);
  myModal.hide();
};

function carregarFormulario() {
    var modalBody = document.getElementById('modalBodyNovoCurso');
    modalBody.innerHTML = 'Carregando...'; // Feedback visual
    fetch('/cursos/formNovoCurso') 
        .then(response => response.text())
        .then(html => {
            modalBody.innerHTML = html;
        })
        .catch(error => {
            modalBody.innerHTML = 'Erro ao carregar o formulário.';
            console.error('Erro:', error);
        });
}

function adicionarTurmaCompleta() {
    const inputNome = document.getElementById('inputNomeTurma');
    const selectTurno = document.getElementById('selectTurnoTurma');
    const container = document.getElementById('listaTurmasDinamic');
    
    const nome = inputNome.value.trim();
    const turno = selectTurno.value;

    if (nome === "") {
        alert("Por favor, digite o nome da turma.");
        return;
    }

    if (container.querySelector('.text-muted')) container.innerHTML = '';

    const div = document.createElement('div');
    div.className = 'badge bg-white text-dark border p-2 d-flex align-items-center shadow-sm';
    
    // O valor enviado será "Nome|Turno" para você separar facilmente no Python
    const valorComposto = `${nome}|${turno}`;
    
    div.innerHTML = `
        <input type="hidden" name="turmas_completas" value="${valorComposto}">
        <span class="me-2"><strong>${nome}</strong> (${turno})</span>
        <button type="button" class="btn-close" style="font-size: 0.5rem" onclick="this.parentElement.remove()"></button>
    `;

    container.appendChild(div);
    inputNome.value = '';
    inputNome.focus();
}