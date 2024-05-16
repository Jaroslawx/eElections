from django.contrib import admin
from .models import ElectionEvent, Candidate, Report

# Rejestracja modeli w panelu administracyjnym
admin.site.register(ElectionEvent)
admin.site.register(Candidate)
admin.site.register(Report)
