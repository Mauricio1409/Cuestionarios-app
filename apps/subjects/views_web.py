from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.subjects.forms import SubjectForm
from apps.subjects.services.subject_service import SubjectService
from core.authz import staff_required


@login_required
def subject_catalog(request):
    subjects = SubjectService().list_subjects()
    return render(request, "catalog/subjects.html", {"subjects": subjects})


@login_required
@staff_required
def subject_create(request):
    form = SubjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        SubjectService().create_subject(form.cleaned_data)
        messages.success(request, "Materia creada correctamente.")
        return redirect("catalog:subjects")

    return render(
        request,
        "common/form.html",
        {
            "form": form,
            "title": "Crear materia",
            "eyebrow": "Staff",
            "description": "Definí una nueva materia para organizar cuestionarios y contenidos.",
            "cancel_url": "/subjects/",
        },
    )


@login_required
@staff_required
def subject_edit(request, subject_id):
    subject = SubjectService().get_subject(subject_id)
    if not subject:
        messages.error(request, "La materia que querés editar no existe.")
        return redirect("catalog:subjects")

    form = SubjectForm(request.POST or None, instance=subject)
    if request.method == "POST" and form.is_valid():
        SubjectService().update_subject(subject, form.cleaned_data)
        messages.success(request, "Materia actualizada correctamente.")
        return redirect("catalog:subjects")

    return render(
        request,
        "common/form.html",
        {
            "form": form,
            "title": "Editar materia",
            "eyebrow": "Staff",
            "description": f"Actualizá los datos de {subject.name} sin salir del flujo editorial del sistema.",
            "cancel_url": "/subjects/",
        },
    )


@login_required
@staff_required
def subject_delete(request, subject_id):
    if request.method != "POST":
        return redirect("catalog:subjects")

    subject = SubjectService().get_subject(subject_id)
    if not subject:
        messages.error(request, "La materia que querés eliminar no existe.")
        return redirect("catalog:subjects")

    subject_name = subject.name
    SubjectService().delete_subject(subject)
    messages.success(request, f"Materia eliminada: {subject_name}.")
    return redirect("catalog:subjects")
