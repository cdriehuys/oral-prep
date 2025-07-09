from django import forms
from django.core.exceptions import ValidationError

from quiz import models


class PreferencesForm(forms.ModelForm):
    certificate_type = forms.CharField(
        widget=forms.RadioSelect(choices=models.Question.CERTIFICATE_TYPES)
    )
    plane_type = forms.CharField(
        required=False,
        widget=forms.RadioSelect(choices={None: "None", **models.Question.PLANE_TYPES}),
    )

    class Meta:
        model = models.Preferences
        fields = ["certificate_type", "plane_type"]


class SearchForm(forms.Form):
    q = forms.CharField(label="Query")
    questions = forms.BooleanField(
        initial=True, label="Search questions", required=False
    )
    answers = forms.BooleanField(initial=False, label="Search answers", required=False)

    def clean(self):
        cleaned_data = super().clean()
        search_questions = cleaned_data.get("questions", False)
        search_answers = cleaned_data.get("answers", False)

        if not (search_questions or search_answers):
            raise ValidationError(
                "A search must include at least questions or answers."
            )
