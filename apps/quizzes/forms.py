from django import forms
from apps.quizzes.models import Quiz, Question, QuestionOption


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["subject", "name", "description", "is_active"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["statement", "image", "question_type", "score", "explanation", "position"]


class QuestionOptionForm(forms.ModelForm):
    class Meta:
        model = QuestionOption
        fields = ["text", "is_correct", "position"]


class AttemptFilterForm(forms.Form):
    user = forms.CharField(required=False)
    quiz = forms.CharField(required=False)
