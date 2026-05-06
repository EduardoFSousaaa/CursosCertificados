function loadTrainingDetail(id) {
    const modalEl = document.getElementById('modalTrainingDetail');
    const modalBody = document.getElementById('modalBodyTrainingDetail');
    if (!modalEl || !modalBody) return;

    modalBody.innerHTML = `
        <div class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Carregando...</span>
            </div>
        </div>`;

    window.bootstrap.Modal.getOrCreateInstance(modalEl).show();

    Http.get(`/trainings/${id}/detail`)
        .then(html => { modalBody.innerHTML = html; })
        .catch(() => {
            modalBody.innerHTML = '<p class="text-danger p-3"><i class="fa-solid fa-circle-exclamation me-2"></i>Erro ao carregar os dados.</p>';
        });
}

function getTrainingModalBody() {
    return document.getElementById('modalBodyNewTraining')
        || document.querySelector('#modalNewTraining .modal-body');
}

function showTrainingModal() {
    const modalEl = document.getElementById('modalNewTraining');
    if (!modalEl) return;
    if (window.bootstrap?.Modal) {
        window.bootstrap.Modal.getOrCreateInstance(modalEl).show();
        return;
    }

    modalEl.classList.add('show');
    modalEl.style.display = 'block';
    modalEl.removeAttribute('aria-hidden');
    document.body.classList.add('modal-open');
}

function loadTrainingForm() {
    const modalBody = getTrainingModalBody();
    if (!modalBody) {
        window.location.href = '/trainings/form';
        return;
    }

    Http.get('/trainings/form')
        .then(html => {
            modalBody.innerHTML = html;
            activateBootstrapValidation();
            initTrainingStepper();
            showTrainingModal();
        })
        .catch(() => {
            modalBody.innerHTML = '<p class="text-danger p-3"><i class="fa-solid fa-circle-exclamation me-2"></i>Erro ao carregar o formulário.</p>';
            showTrainingModal();
        });
}

function activateBootstrapValidation() {
    const form = document.getElementById('formNewTraining');
    if (!form) return;
    form.addEventListener('submit', (e) => {
        if (!form.checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
        }
        form.classList.add('was-validated');
    });
}

function initTrainingStepper() {
    const form = document.getElementById('formNewTraining');
    if (!form) return;

    const steps = Array.from(form.querySelectorAll('.training-step'));
    const stepButtons = Array.from(form.querySelectorAll('[data-stepper] .step'));
    let currentStep = 1;

    const startsOnInput = form.querySelector('#starts_on');
    const endsOnInput   = form.querySelector('#ends_on');

    function syncDateConstraint() {
        if (!startsOnInput || !endsOnInput) return;
        endsOnInput.min = startsOnInput.value || '';
    }

    function validateDateRange() {
        if (!startsOnInput || !endsOnInput) return true;
        if (!startsOnInput.value || !endsOnInput.value) return true;

        const valid = endsOnInput.value >= startsOnInput.value;
        const feedback = endsOnInput.closest('.col-md-6, .col-12')
            ?.querySelector('.invalid-feedback');

        if (!valid) {
            endsOnInput.setCustomValidity('A data de término não pode ser anterior à data de início.');
            if (feedback) feedback.textContent = 'A data de término não pode ser anterior à data de início.';
        } else {
            endsOnInput.setCustomValidity('');
            if (feedback) feedback.textContent = feedback.dataset.defaultMsg || '';
        }
        return valid;
    }

    if (startsOnInput) {
        startsOnInput.addEventListener('change', () => {
            syncDateConstraint();
            validateDateRange();
        });
    }
    if (endsOnInput) {
        endsOnInput.addEventListener('change', validateDateRange);
    }

    const showStep = (step) => {
        currentStep = step;
        steps.forEach((el) => {
            const isActive = Number(el.dataset.step) === step;
            el.classList.toggle('is-active', isActive);
        });
        stepButtons.forEach((btn) => {
            const isActive = Number(btn.dataset.step) === step;
            btn.classList.toggle('active', isActive);
        });
        if (step === 4) {
            buildTrainingReview();
        }
    };

    const validateStep1 = () => {
        if (!form.checkValidity()) {
            form.classList.add('was-validated');
            return false;
        }
        if (!validateDateRange()) {
            form.classList.add('was-validated');
            return false;
        }
        return true;
    };

    const nextButtons = form.querySelectorAll('[data-stepper-next]');
    const prevButtons = form.querySelectorAll('[data-stepper-prev]');

    nextButtons.forEach((btn) => {
        btn.addEventListener('click', () => {
            if (currentStep === 1 && !validateStep1()) return;
            showStep(Math.min(currentStep + 1, steps.length));
        });
    });

    prevButtons.forEach((btn) => {
        btn.addEventListener('click', () => {
            showStep(Math.max(currentStep - 1, 1));
        });
    });

    stepButtons.forEach((btn) => {
        btn.addEventListener('click', () => {
            const targetStep = Number(btn.dataset.step);
            if (targetStep > currentStep && currentStep === 1 && !validateStep1()) return;
            showStep(targetStep);
        });
    });

    showStep(1);
}

function buildTrainingReview() {
    const container = document.getElementById('trainingReviewList');
    if (!container) return;

    const getValue = (id) => {
        const el = document.getElementById(id);
        return el ? el.value.trim() : '';
    };

    const classGroups = Array.from(document.querySelectorAll('[name="class_groups"]'))
        .map((el) => el.value.replace('|', ' / '));

    const items = [
        { label: 'Titulo', value: getValue('title') || '—' },
        { label: 'Inicio', value: getValue('starts_on') || '—' },
        { label: 'Termino', value: getValue('ends_on') || '—' },
        { label: 'Carga horaria', value: getValue('duration_minutes') || '—' },
        { label: 'Situacao', value: getValue('status') || '—' },
        { label: 'Local', value: getValue('location') || '—' },
        { label: 'Endereco', value: getValue('address') || '—' },
        { label: 'Formulario online', value: getValue('online_form_url') || '—' },
        { label: 'Turmas', value: classGroups.length ? classGroups.join(', ') : '—' },
        { label: 'Conteudo', value: getValue('description') || '—' },
        { label: 'Competencias clinicas', value: getValue('clinical_skills') || '—' },
        { label: 'Materiais', value: getValue('required_materials') || '—' },
        { label: 'Pre-requisitos', value: getValue('prerequisites') || '—' },
    ];

    container.innerHTML = items
        .map((item) => (
            `<div class="review-item"><span>${escapeHtml(item.label)}:</span><strong>${escapeHtml(item.value)}</strong></div>`
        ))
        .join('');
}

function addClassGroup() {
    const inputName = document.getElementById('inputGroupName');
    const selectShift = document.getElementById('selectGroupShift');
    const container = document.getElementById('classGroupList');
    const emptyMsg = document.getElementById('classGroupEmptyMsg');

    const name = inputName.value.trim();
    if (!name) { inputName.classList.add('is-invalid'); return; }
    inputName.classList.remove('is-invalid');

    if (emptyMsg) emptyMsg.remove();

    const shiftLabels = { morning: 'Manhã', afternoon: 'Tarde', evening: 'Noite' };
    const shift = selectShift.value;

    const badge = document.createElement('div');
    badge.className = 'badge bg-white text-dark border p-2 d-flex align-items-center gap-2 shadow-sm';
    badge.innerHTML = `
        <input type="hidden" name="class_groups" value="${escapeHtml(name)}|${escapeHtml(shift)}">
        <span><strong>${escapeHtml(name)}</strong> (${escapeHtml(shiftLabels[shift] || shift)})</span>
        <button type="button" class="btn-close" style="font-size:0.5rem"
                onclick="this.closest('.badge').remove(); checkClassGroupEmpty();"
                aria-label="Remover"></button>`;

    container.appendChild(badge);
    inputName.value = '';
    inputName.focus();
}

function checkClassGroupEmpty() {
    const container = document.getElementById('classGroupList');
    if (!container.querySelector('[name="class_groups"]')) {
        const span = document.createElement('span');
        span.id = 'classGroupEmptyMsg';
        span.className = 'text-muted small align-self-center';
        span.textContent = 'Nenhuma turma definida.';
        container.appendChild(span);
    }
}
