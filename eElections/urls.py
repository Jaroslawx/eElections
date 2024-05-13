from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView

from base.views import home, signup, login, logout
from base.views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, \
    CustomPasswordResetCompleteView

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),


    path("accounts/signup/", signup, name="signup"),
    path("accounts/login/", login, name='login'),
    path("accounts/logout/", logout, name='logout'),

    path("accounts/password_reset/", CustomPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='custom_password_reset_confirm'),
    path('accounts/reset/done', CustomPasswordResetCompleteView.as_view(), name='custom_password_reset_complete'),

    path('base/', include('base.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    # TODO: zapytac czy to lepiej, zeby bylo w base/urls.py?

]
