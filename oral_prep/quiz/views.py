import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from quiz import models

@login_required
def home_view(req):
    question_count = models.Question.objects.count()
    question = models.Question.objects.all()[random.randint(0, question_count-1)]
    context = {
        "question": question
    }

    return render(req, template_name="quiz/home.html", context=context)
