from django import forms

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
