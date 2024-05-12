from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from base.views import home

from base.views import signup, login

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('base/', include('base.urls')),
    path("accounts/signup/", signup, name="signup"),
    path("accounts/login/", login, name='login'),
    path('accounts/', include('django.contrib.auth.urls')),

    # TODO: zapytac czy to lepiej, zeby bylo w base/urls.py?

]
