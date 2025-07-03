import random
from django.shortcuts import render

from quiz import models

def home_view(req):
    question_count = models.Question.objects.count()
    question = models.Question.objects.all()[random.randint(0, question_count-1)]
    context = {
        "question": question
    }

    return render(req, template_name="quiz/home.html", context=context)
