from django.contrib import admin
from .models import ElectionEvent, Candidate, Report, Vote


class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 1


class ElectionEventAdmin(admin.ModelAdmin):
    list_display = ('id_election', 'type', 'start_date', 'end_date')
    list_filter = ('type', 'start_date', 'end_date')
    search_fields = ('type',)
    filter_horizontal = ('eligible_voters',)
    inlines = [CandidateInline]


class CandidateAdmin(admin.ModelAdmin):
    list_display = ('id_candidate', 'name', 'surname', 'description', 'id_election', 'votes')
    list_filter = ('id_election',)
    search_fields = ('name', 'surname')


class ReportAdmin(admin.ModelAdmin):
    list_display = ('id_report', 'id_election', 'csv_file', 'frequency')
    list_filter = ('id_election',)
    search_fields = ('id_election__type',)


class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'id_election')
    list_filter = ('id_election',)
    search_fields = ('user__username', 'id_election__type')


admin.site.register(ElectionEvent, ElectionEventAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Vote, VoteAdmin)
