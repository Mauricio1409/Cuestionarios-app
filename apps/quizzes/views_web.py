from django.contrib import messages
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
        messages.success(request, "Cuestionario creado correctamente. Ahora podés cargar sus preguntas.")
        return redirect("admin-ui:quiz-list")
    return render(
        request,
        "common/form.html",
        {
            "form": form,
            "title": "Crear cuestionario",
            "eyebrow": "Staff",
            "description": "Primero definí el cuestionario y después cargá sus preguntas una por una.",
            "cancel_url": "/staff/quizzes/",
        },
    )


@login_required
@staff_required
def admin_quiz_edit(request, quiz_id):
    service = QuizAdminService()
    try:
        quiz = service.get_quiz(quiz_id)
    except Exception as exc:
        messages.error(request, str(exc))
        return redirect("admin-ui:quiz-list")

    form = QuizForm(request.POST or None, instance=quiz)
    if request.method == "POST" and form.is_valid():
        service.update_quiz(quiz_id, form.cleaned_data)
        messages.success(request, "Cuestionario actualizado correctamente.")
        return redirect("admin-ui:quiz-list")

    return render(
        request,
        "common/form.html",
        {
            "form": form,
            "title": "Editar cuestionario",
            "eyebrow": "Staff",
            "description": f"Ajustá los datos principales de {quiz.name} antes de seguir con sus preguntas.",
            "cancel_url": "/staff/quizzes/",
        },
    )


@login_required
@staff_required
def admin_quiz_delete(request, quiz_id):
    if request.method != "POST":
        return redirect("admin-ui:quiz-list")

    try:
        quiz = QuizAdminService().get_quiz(quiz_id)
        quiz_name = quiz.name
        QuizAdminService().delete_quiz(quiz_id)
        messages.success(request, f"Cuestionario eliminado: {quiz_name}.")
    except Exception as exc:
        messages.error(request, str(exc))
    return redirect("admin-ui:quiz-list")


@login_required
@staff_required
def admin_question_list(request, quiz_id):
    try:
        quiz, questions = QuizAdminService().list_questions(quiz_id)
    except Exception as exc:
        messages.error(request, str(exc))
        return redirect("admin-ui:quiz-list")

    return render(request, "admin_ui/question_list.html", {"quiz": quiz, "questions": questions})


@login_required
@staff_required
def admin_question_create(request, quiz_id):
    try:
        quiz = QuizAdminService().get_quiz(quiz_id)
    except Exception as exc:
        messages.error(request, str(exc))
        return redirect("admin-ui:quiz-list")

    form = QuestionForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        try:
            QuizAdminService().create_question(quiz_id, form.cleaned_data)
            messages.success(request, "Pregunta creada correctamente.")
            return redirect("admin-ui:question-list", quiz_id=quiz_id)
        except Exception as exc:
            form.add_error(None, str(exc))
    return render(
        request,
        "common/form.html",
        {
            "form": form,
            "title": "Crear pregunta",
            "eyebrow": quiz.name,
            "description": "Definí el enunciado, el tipo de respuesta y el puntaje de esta pregunta.",
            "cancel_url": f"/staff/quizzes/{quiz_id}/questions/",
        },
    )


@login_required
@staff_required
def admin_question_edit(request, question_id):
    service = QuizAdminService()
    try:
        question = service.get_question(question_id)
    except Exception as exc:
        messages.error(request, str(exc))
        return redirect("admin-ui:quiz-list")

    form = QuestionForm(request.POST or None, request.FILES or None, instance=question)
    if request.method == "POST" and form.is_valid():
        try:
            service.update_question(question_id, form.cleaned_data)
            messages.success(request, "Pregunta actualizada correctamente.")
            return redirect("admin-ui:question-list", quiz_id=question.quiz_id)
        except Exception as exc:
            form.add_error(None, str(exc))

    return render(
        request,
        "common/form.html",
        {
            "form": form,
            "title": "Editar pregunta",
            "eyebrow": question.quiz.name,
            "description": "Ajustá el enunciado, el tipo o el puntaje sin perder el contexto del cuestionario.",
            "cancel_url": f"/staff/quizzes/{question.quiz_id}/questions/",
        },
    )


@login_required
@staff_required
def admin_question_delete(request, question_id):
    if request.method != "POST":
        return redirect("admin-ui:quiz-list")

    try:
        question = QuizAdminService().get_question(question_id)
        quiz_id = question.quiz_id
        label = question.statement or f"Pregunta {question.position}"
        QuizAdminService().delete_question(question_id)
        messages.success(request, f"Pregunta eliminada: {label[:60]}.")
        return redirect("admin-ui:question-list", quiz_id=quiz_id)
    except Exception as exc:
        messages.error(request, str(exc))
        return redirect("admin-ui:quiz-list")


@login_required
@staff_required
def admin_option_create(request, question_id):
    option_service = QuestionOptionService()
    try:
        question = QuizAdminService().get_question(question_id)
    except Exception as exc:
        messages.error(request, str(exc))
        return redirect("admin-ui:quiz-list")

    form = QuestionOptionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            option_service.create_for_question(question_id, form.cleaned_data)
            messages.success(request, "Opción creada correctamente.")
            return redirect("admin-ui:option-list", question_id=question_id)
        except Exception as exc:
            form.add_error(None, str(exc))
    return render(
        request,
        "common/form.html",
        {
            "form": form,
            "title": "Crear opción",
            "eyebrow": question.quiz.name,
            "description": "Cargá una opción para esta pregunta y marcá si cuenta como correcta.",
            "cancel_url": f"/staff/questions/{question_id}/options/",
        },
    )


@login_required
@staff_required
def admin_option_list(request, question_id):
    service = QuestionOptionService()
    try:
        question, options = service.list_for_question(question_id)
    except Exception as exc:
        messages.error(request, str(exc))
        return redirect("admin-ui:quiz-list")

    return render(request, "admin_ui/option_list.html", {"question": question, "options": options})


@login_required
@staff_required
def admin_option_edit(request, option_id):
    service = QuestionOptionService()
    try:
        option = service.get_option(option_id)
    except Exception as exc:
        messages.error(request, str(exc))
        return redirect("admin-ui:quiz-list")

    form = QuestionOptionForm(request.POST or None, instance=option)
    if request.method == "POST" and form.is_valid():
        try:
            service.update_option(option_id, form.cleaned_data)
            messages.success(request, "Opción actualizada correctamente.")
            return redirect("admin-ui:option-list", question_id=option.question_id)
        except Exception as exc:
            form.add_error(None, str(exc))

    return render(
        request,
        "common/form.html",
        {
            "form": form,
            "title": "Editar opción",
            "eyebrow": option.question.quiz.name,
            "description": "Ajustá el texto, la posición o si la opción cuenta como correcta.",
            "cancel_url": f"/staff/questions/{option.question_id}/options/",
        },
    )


@login_required
@staff_required
def admin_option_delete(request, option_id):
    if request.method != "POST":
        return redirect("admin-ui:quiz-list")

    service = QuestionOptionService()
    try:
        option = service.get_option(option_id)
        question_id = option.question_id
        label = option.text
        service.delete_option(option_id)
        messages.success(request, f"Opción eliminada: {label[:60]}.")
        return redirect("admin-ui:option-list", question_id=question_id)
    except Exception as exc:
        messages.error(request, str(exc))
        return redirect("admin-ui:quiz-list")
