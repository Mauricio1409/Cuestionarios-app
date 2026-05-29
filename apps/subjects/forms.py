from django import forms
from apps.subjects.models import Subject


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "description"]
