from django.urls import path
from . import views


urlpatterns = [
    path("all_elections/", views.all_elections, name="all_elections"),
    path("vote/<int:election_id>/", views.vote, name="vote"),
    path("thank_you/", views.thank_you, name="thank_you"),

    path("admin_elections/", views.admin_elections, name="admin_elections"),
]
