from django.core.exceptions import ValidationError
from apps.quizzes.repositories.quiz_repository import QuizRepository
from apps.quizzes.repositories.question_repository import QuestionOptionRepository, QuestionRepository
from apps.quizzes.models import QuestionType


class QuizService:
    def __init__(self):
        self.repo = QuizRepository()

    def list_admin(self):
        return self.repo.list_all()

    def list_catalog(self):
        return self.repo.list_active()

    def create(self, data):
        return self.repo.create(**data)

    def update(self, quiz, data):
        return self.repo.update(quiz, **data)

    def can_take(self, quiz):
        return quiz.is_active and self.repo.has_questions(quiz)

    def get_quiz(self, quiz_id: int):
        return self.repo.get(quiz_id)


class QuestionDomainService:
    def validate_question_content(self, statement, image):
        if not statement and not image:
            raise ValidationError("La pregunta debe tener texto, imagen o ambos.")

    def validate_correct_options(self, question, options):
        correct_count = sum(1 for o in options if o.is_correct)
        if question.question_type == QuestionType.SINGLE_CHOICE and correct_count != 1:
            raise ValidationError("Una pregunta single_choice debe tener exactamente una opción correcta.")
        if question.question_type == QuestionType.MULTIPLE_CHOICE and correct_count < 1:
            raise ValidationError("Una pregunta multiple_choice debe tener al menos una opción correcta.")


class QuestionOptionService:
    def __init__(self):
        self.option_repo = QuestionOptionRepository()
        self.question_repo = QuestionRepository()
        self.domain = QuestionDomainService()

    def validate_and_persist_option(self, question, data, option=None):
        obj = self.option_repo.update(option, **data) if option else self.option_repo.create(question=question, **data)
        options = list(self.option_repo.by_question(question.id))
        self.domain.validate_correct_options(question, options)
        return obj

    def create_for_question(self, question_id, data):
        question = self.question_repo.get(question_id)
        if not question:
            raise ValidationError("Pregunta no encontrada.")
        return self.validate_and_persist_option(question, data)


class QuizAdminService:
    def __init__(self):
        self.quiz_repo = QuizRepository()
        self.question_repo = QuestionRepository()
        self.domain = QuestionDomainService()

    def create_quiz(self, data):
        return self.quiz_repo.create(**data)

    def update_quiz(self, quiz_id, data):
        quiz = self.quiz_repo.get(quiz_id)
        if not quiz:
            raise ValidationError("Quiz no encontrado.")
        return self.quiz_repo.update(quiz, **data)

    def delete_quiz(self, quiz_id):
        quiz = self.quiz_repo.get(quiz_id)
        if not quiz:
            raise ValidationError("Quiz no encontrado.")
        self.quiz_repo.delete(quiz)

    def get_quiz(self, quiz_id):
        quiz = self.quiz_repo.get(quiz_id)
        if not quiz:
            raise ValidationError("Quiz no encontrado.")
        return quiz

    def list_questions(self, quiz_id):
        quiz = self.get_quiz(quiz_id)
        questions = self.question_repo.by_quiz(quiz_id)
        return quiz, questions

    def create_question(self, quiz_id, data):
        quiz = self.quiz_repo.get(quiz_id)
        if not quiz:
            raise ValidationError("Quiz no encontrado.")
        self.domain.validate_question_content(data.get("statement"), data.get("image"))
        return self.question_repo.create(quiz=quiz, **data)

    def update_question(self, question_id, data):
        question = self.question_repo.get(question_id)
        if not question:
            raise ValidationError("Pregunta no encontrada.")
        self.domain.validate_question_content(data.get("statement"), data.get("image") or question.image)
        return self.question_repo.update(question, **data)

    def delete_question(self, question_id):
        question = self.question_repo.get(question_id)
        if not question:
            raise ValidationError("Pregunta no encontrada.")
        quiz_id = question.quiz_id
        self.question_repo.delete(question)
        return quiz_id

    def get_question(self, question_id):
        question = self.question_repo.get(question_id)
        if not question:
            raise ValidationError("Pregunta no encontrada.")
        return question
