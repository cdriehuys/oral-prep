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
