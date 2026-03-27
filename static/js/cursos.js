function fechamodal(strModal) {
  const myModalElement = document.getElementById(strModal);
  const myModal = bootstrap.Modal.getInstance(myModalElement);
  myModal.hide();
};

function NovoCurso(){
  // Script para carregar o conteúdo via AJAX
  const meuModal = document.getElementById('ModalNovoCurso');
  meuModal.addEventListener('show.bs.modal', function (event) {
    const modalBody = document.getElementById('modalBody');
    
    // Faz a requisição para o arquivo do formulário
    fetch('templates/addCurso.html')
      .then(response => response.text())
      .then(html => {
        modalBody.innerHTML = html; // Insere o HTML no modal
      })
      .catch(error => {
        modalBody.innerHTML = 'Erro ao carregar o formulário.';
      });
  });
};
