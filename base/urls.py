from django.urls import include, path, re_path
from . import views

from base.views import signup, logout
from base.views import CustomLoginView, CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, \
    CustomPasswordResetCompleteView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("all_elections/", views.all_elections, name="all_elections"),
    path("vote/<int:election_id>/", views.vote, name="vote"),
    path("thank_you/", views.thank_you, name="thank_you"),

    path("signup/", signup, name="signup"),
    path("logout/", logout, name='logout'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path("password_reset/", CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='custom_password_reset_confirm'),
    path('reset/done', CustomPasswordResetCompleteView.as_view(), name='custom_password_reset_complete'),
    path('accounts/', include('django.contrib.auth.urls')),

    path("admin_elections/", views.admin_elections, name="admin_elections"),
    path("admin_eligible/<int:election_id>/", views.admin_eligible, name="admin_eligible"),

]
