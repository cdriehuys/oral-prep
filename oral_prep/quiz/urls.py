from django.urls import path

from quiz import views

urlpatterns = [
    path("about", views.about_view, name="about"),
    path("preferences", views.preferences_view, name="preferences"),
    path(
        "questions/<int:question_id>",
        views.question_detail_view,
        name="question-detail",
    ),
    path("search", views.search_view, name="search"),
    path("", views.home_view, name="home"),
]
