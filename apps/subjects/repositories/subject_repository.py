from django.db.models import Count, Q

from apps.subjects.models import Subject


class SubjectRepository:
    def list_all(self):
        return Subject.objects.annotate(
            active_quiz_count=Count("quizzes", filter=Q(quizzes__is_active=True), distinct=True)
        )

    def get(self, pk: int):
        return Subject.objects.filter(pk=pk).first()

    def create(self, **data):
        return Subject.objects.create(**data)

    def update(self, subject: Subject, **data):
        for k, v in data.items():
            setattr(subject, k, v)
        subject.save()
        return subject

    def delete(self, subject: Subject):
        subject.delete()
