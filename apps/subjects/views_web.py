from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.subjects.services.subject_service import SubjectService


@login_required
def subject_catalog(request):
    subjects = SubjectService().list_subjects()
    return render(request, "catalog/subjects.html", {"subjects": subjects})
