from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.attempts.services.attempt_service import AttemptService
from apps.quizzes.forms import AttemptFilterForm
from core.authz import staff_required


@login_required
def start_attempt(request, quiz_id):
    try:
        attempt = AttemptService().start_attempt(request.user, quiz_id)
        return redirect("attempts:take", attempt_id=attempt.id)
    except Exception as exc:
        messages.error(request, str(exc))
        return redirect("quizzes:quizzes")


@login_required
def take_attempt(request, attempt_id):
    attempt = AttemptService().get_user_attempt_or_404(request.user.id, attempt_id)
    questions = attempt.quiz.questions.prefetch_related("options").order_by("position")
    return render(request, "attempts/take.html", {"attempt": attempt, "questions": questions})


@login_required
def submit_attempt(request, attempt_id):
    attempt = AttemptService().get_user_attempt_or_404(request.user.id, attempt_id)
    payload = {str(q.id): request.POST.getlist(f"question_{q.id}") for q in attempt.quiz.questions.all()}
    AttemptService().submit_attempt(attempt, payload)
    return redirect("attempts:detail", attempt_id=attempt.id)


@login_required
def history_view(request):
    attempts = AttemptService().history_for_user(request.user.id)
    return render(request, "attempts/history.html", {"attempts": attempts})


@login_required
def attempt_detail(request, attempt_id):
    attempt = AttemptService().detail_for_user(attempt_id, request.user.id)
    if not attempt:
        messages.error(request, "No tenés permiso para ver ese intento o no existe.")
        return redirect("attempts:history")
    return render(request, "attempts/detail.html", {"attempt": attempt})


@login_required
@staff_required
def admin_attempt_list(request):
    form = AttemptFilterForm(request.GET or None)
    user_q = form.data.get("user") if form.is_bound else None
    quiz_q = form.data.get("quiz") if form.is_bound else None
    attempts = AttemptService().admin_list(user_q=user_q, quiz_q=quiz_q)
    return render(request, "admin_ui/attempt_list.html", {"attempts": attempts, "form": form})
