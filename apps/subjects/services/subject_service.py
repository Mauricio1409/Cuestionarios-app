from django.core.exceptions import ValidationError

from apps.subjects.repositories.subject_repository import SubjectRepository


class SubjectService:
    def __init__(self):
        self.repo = SubjectRepository()

    def list_subjects(self):
        return self.repo.list_all()

    def create_subject(self, data):
        if not data.get("name") or not str(data.get("name")).strip():
            raise ValidationError("El nombre de la materia es obligatorio.")
        return self.repo.create(**data)

    def update_subject(self, subject, data):
        return self.repo.update(subject, **data)
