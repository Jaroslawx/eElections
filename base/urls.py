from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("all_elections/", views.all_elections, name="all_elections"),
    path("vote/<int:election_id>/", views.vote, name="vote"),
    path("thank_you/", views.thank_you, name="thank_you"),
    # path("login/", views.login, name='login'),
    # path("signup/", views.signup, name='signup'),

]
