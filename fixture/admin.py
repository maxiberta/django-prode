from fixture.models import *
from django.contrib import admin

class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name',]

class MatchAdmin(admin.ModelAdmin):
    list_display = ['tournament', '__unicode__', 'start', 'location']
    list_filter = ['tournament']

class TeamAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Team, TeamAdmin)
