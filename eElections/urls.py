from django.contrib import admin
from django.urls import include, path, re_path

from base.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('base/', include('base.urls')),
    path('elections/', include('base.urls')),
    path('accounts/', include('base.urls')),

]
