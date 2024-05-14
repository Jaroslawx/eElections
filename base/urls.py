from django.urls import include, path, re_path
from . import views

from base.views import signup, login, logout
from base.views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, \
    CustomPasswordResetCompleteView


urlpatterns = [
    path("", views.home, name="home"),
    path("all_elections/", views.all_elections, name="all_elections"),
    path("vote/<int:election_id>/", views.vote, name="vote"),
    path("thank_you/", views.thank_you, name="thank_you"),

    path("accounts/signup/", signup, name="signup"),
    path("accounts/login/", login, name='login'),
    path("accounts/logout/", logout, name='logout'),

    path("accounts/password_reset/", CustomPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='custom_password_reset_confirm'),
    path('accounts/reset/done', CustomPasswordResetCompleteView.as_view(), name='custom_password_reset_complete'),
    path('accounts/', include('django.contrib.auth.urls')),

]
