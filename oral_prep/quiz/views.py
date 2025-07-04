import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from quiz import models

@login_required
def home_view(req):
    preferences = models.Preferences.for_user(req.user)
    questions = preferences.get_applicable_questions()
    question_count = questions.count()
    question = questions.all()[random.randint(0, question_count-1)]
    context = {
        "question": question
    }

    return render(req, template_name="quiz/home.html", context=context)
