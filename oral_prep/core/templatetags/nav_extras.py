from django import template
from django.urls import reverse
from django.utils.html import format_html

register = template.Library()


@register.simple_tag(takes_context=True)
def navlink(context, text: str, url_name: str):
    request = context["request"]
    url = reverse(url_name)
    active = request.path == url

    classes = ["navlink"]
    if active:
        classes.append("navlink--active")

    return format_html(
        '<li class="{}"><a href="{}">{}</a></li>',
        " ".join(classes),
        url,
        text,
    )
