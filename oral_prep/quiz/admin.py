from django.contrib import admin

from quiz import models

@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ("certificate_type", "plane_type", "question", "answer", "image", "import_id")
    list_display = ("question", "certificate_type", "plane_type", "import_id")
