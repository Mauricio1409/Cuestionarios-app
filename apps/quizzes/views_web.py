from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.quizzes.forms import QuizForm, QuestionForm, QuestionOptionForm
from apps.quizzes.services.quiz_service import QuizService, QuestionOptionService, QuizAdminService
from core.authz import StaffRequiredMixin, staff_required
from django.views.generic import TemplateView


@login_required
def quiz_catalog(request):
    quizzes = QuizService().list_catalog()
    return render(request, "catalog/quizzes.html", {"quizzes": quizzes})


class AdminDashboardView(StaffRequiredMixin, TemplateView):
    template_name = "admin_ui/dashboard.html"


@login_required
@staff_required
def admin_quiz_list(request):
    return render(request, "admin_ui/quiz_list.html", {"quizzes": QuizService().list_admin()})


@login_required
@staff_required
def admin_quiz_create(request):
    form = QuizForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        QuizAdminService().create_quiz(form.cleaned_data)
        return redirect("admin-ui:quiz-list")
    return render(request, "common/form.html", {"form": form, "title": "Crear quiz"})


@login_required
@staff_required
def admin_question_create(request, quiz_id):
    form = QuestionForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        try:
            QuizAdminService().create_question(quiz_id, form.cleaned_data)
            return redirect("admin-ui:quiz-list")
        except Exception as exc:
            form.add_error(None, str(exc))
    return render(request, "common/form.html", {"form": form, "title": "Crear pregunta"})


@login_required
@staff_required
def admin_option_create(request, question_id):
    form = QuestionOptionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            QuestionOptionService().create_for_question(question_id, form.cleaned_data)
            return redirect("admin-ui:quiz-list")
        except Exception as exc:
            form.add_error(None, str(exc))
    return render(request, "common/form.html", {"form": form, "title": "Crear opción"})
