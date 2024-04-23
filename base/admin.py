from django.contrib import admin
from .models import Election, Candidate, Report

# Rejestracja modeli w panelu administracyjnym
admin.site.register(Election)
admin.site.register(Candidate)
admin.site.register(Report)
