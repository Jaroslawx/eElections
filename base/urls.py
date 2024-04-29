from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("all_elections/", views.all_elections, name="all_elections"),
    path("vote/", views.vote, name="vote")
]
