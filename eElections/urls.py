from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("base/", include("base.urls")),
    path('admin/', admin.site.urls),
]
