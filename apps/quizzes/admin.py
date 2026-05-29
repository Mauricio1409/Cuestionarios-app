from django.contrib import admin
from apps.quizzes.models import Quiz, Question, QuestionOption

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(QuestionOption)
