from apps.quizzes.models import Question, QuestionOption


class QuestionRepository:
    def by_quiz(self, quiz_id: int):
        return Question.objects.filter(quiz_id=quiz_id).order_by("position", "id")

    def get(self, pk: int):
        return Question.objects.filter(pk=pk).first()

    def create(self, **data):
        return Question.objects.create(**data)

    def update(self, question: Question, **data):
        for k, v in data.items():
            setattr(question, k, v)
        question.save()
        return question

    def delete(self, question: Question):
        question.delete()


class QuestionOptionRepository:
    def by_question(self, question_id: int):
        return QuestionOption.objects.filter(question_id=question_id).order_by("position", "id")

    def get(self, pk: int):
        return QuestionOption.objects.filter(pk=pk).first()

    def create(self, **data):
        return QuestionOption.objects.create(**data)

    def update(self, option: QuestionOption, **data):
        for k, v in data.items():
            setattr(option, k, v)
        option.save()
        return option

    def delete(self, option: QuestionOption):
        option.delete()
