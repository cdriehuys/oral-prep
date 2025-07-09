import random

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

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


@login_required
def question_detail_view(request, question_id: int):
    question = get_object_or_404(models.Question, id=question_id)
    context = {"question": question}

    return render(request, template_name="quiz/question-detail.html", context=context)


@login_required
def search_view(request):
    if "q" in request.GET:
        form = forms.SearchForm(request.GET)
    else:
        form = forms.SearchForm()

    context = {"form": form}

    if form.is_valid():
        search_term = form.cleaned_data["q"]
        search_questions = form.cleaned_data["questions"]
        search_answer = form.cleaned_data["answers"]

        query = Q()
        if search_questions:
            query |= Q(question__icontains=search_term)

        if search_answer:
            query |= Q(answer__icontains=search_term)

        context["query"] = search_term
        context["questions"] = models.Question.objects.filter(query).order_by("id")

    return render(request, template_name="quiz/search.html", context=context)
