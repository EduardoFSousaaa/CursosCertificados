from app.exceptions.app_errors import NotFoundError
from app.forms.training_form import TrainingForm
from app.models.training import Training
from app.repositories.training_repository import TrainingRepository
from app.utils.enums import TrainingStatus


class TrainingService:
    @staticmethod
    def list_all() -> list[Training]:
        return TrainingRepository.find_all()

    @staticmethod
    def create(form: TrainingForm) -> Training:
        training = Training(
            title=form.title.data,
            starts_on=form.starts_on.data,
            ends_on=form.ends_on.data,
            duration_minutes=form.duration_minutes.data,
            location=form.location.data,
            address=form.address.data,
            online_form_url=form.online_form_url.data,
            description=form.description.data,
            clinical_skills=form.clinical_skills.data,
            required_materials=form.required_materials.data,
            prerequisites=form.prerequisites.data,
            status=TrainingStatus(form.status.data),
            instructor_id=form.instructor_id.data or None,
        )
        return TrainingRepository.save(training)

    @staticmethod
    def get_by_id(id: int) -> Training:
        return TrainingRepository.find_by_id_or_404(id)

    @staticmethod
    def remove(id: int) -> None:
        training = TrainingRepository.find_by_id(id)
        if training is None:
            raise NotFoundError(f"Treinamento {id} não encontrado.")
        TrainingRepository.delete(training)
