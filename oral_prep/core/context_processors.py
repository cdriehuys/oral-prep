from django.conf import settings


def maintainer_info(_request):
    return {
        "MAINTAINER_NAME": settings.MAINTAINER_NAME,
        "MAINTAINER_EMAIL": settings.MAINTAINER_EMAIL,
    }
