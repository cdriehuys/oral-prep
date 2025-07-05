from django.urls import path

from quiz import views

urlpatterns = [
    path("about", views.about_view, name="about"),
    path("preferences", views.preferences_view, name="preferences"),
    path("", views.home_view, name="home"),
]
