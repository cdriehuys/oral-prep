from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

class Question(models.Model):

    CERTIFICATE_TYPES = {
        "PRIVATE": _("Private"),
        "COMMERCIAL": _("Commercial"),
    }

    PLANE_TYPES = {
        "ALL": _("All"),
        "C152": _("Cessna 152"),
        "C172": _("Cessna 172"),
        "WARRIOR": _("Piper Warrior"),
        "MOONEY": _("Mooney M20J"),
    }

    certificate_type = models.CharField(choices=CERTIFICATE_TYPES, null=False, verbose_name=_("certificate type"))
    plane_type = models.CharField(choices=PLANE_TYPES, null=False, verbose_name=_("plane type"))

    question = models.TextField(null=False, verbose_name=_("question"))
    answer = models.TextField(null=False, verbose_name=_("answer"))

    image = models.ImageField(blank=True, null=True, verbose_name=_("image"))

    import_id = models.IntegerField(blank=True, null=True, unique=True, verbose_name=_("import ID"))


class Preferences(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_preferences")

    certificate_type = models.CharField(choices=Question.CERTIFICATE_TYPES, default="PRIVATE", verbose_name=_("certificate type"))
    plane_type = models.CharField(choices=Question.PLANE_TYPES, default=None, null=True, verbose_name=_("plane type"))

    @classmethod
    def for_user(cls, user):
        preferences, _ = cls.objects.get_or_create(user=user)
        return preferences

    def get_applicable_questions(self):
        questions = Question.objects.all()

        if self.certificate_type == "PRIVATE":
            questions = questions.filter(certificate_type=self.certificate_type)

        if self.plane_type is None:
            questions = questions.filter(plane_type="ALL")
        elif self.plane_type != "ALL":
            questions = questions.filter(plane_type__in=["ALL", self.plane_type])

        return questions

