import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from quiz import forms, models


def about_view(request):
    return render(request, template_name="quiz/about.html")


@login_required
def home_view(req):
    preferences = models.Preferences.for_user(req.user)
    questions = preferences.get_applicable_questions()
    question_count = questions.count()
    question = questions.all()[random.randint(0, question_count - 1)]
    context = {"question": question}

    return render(req, template_name="quiz/home.html", context=context)


@login_required
def preferences_view(request):
    preferences = models.Preferences.for_user(request.user)

    if request.method == "POST":
        form = forms.PreferencesForm(request.POST, instance=preferences)
        if form.is_valid():
            form.save()
    else:
        form = forms.PreferencesForm(instance=preferences)

    context = {"form": form}

    return render(request, template_name="quiz/preferences.html", context=context)
