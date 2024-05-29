from django.urls import path
from . import views


urlpatterns = [
    path("all_elections/", views.all_elections, name="all_elections"),
    path("vote/<int:election_id>/", views.vote, name="vote"),
    path('results/<int:election_id>/', views.election_results, name='election_results'),
    path("thank_you/", views.thank_you, name="thank_you"),
    path('api/upcoming_elections/', views.upcoming_elections, name='upcoming_elections'),

    path("admin_elections/", views.admin_elections, name="admin_elections"),
]
