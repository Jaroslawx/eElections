from django.contrib import admin
from django.urls import include, path
from base.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('base/', include('base.urls')),
]
