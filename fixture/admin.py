from fixture.models import *
from django.contrib import admin

class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name',]

class MatchAdmin(admin.ModelAdmin):
    list_display = ['tournament', '__unicode__', 'start', 'location']
    list_filter = ['tournament']

class TeamAdmin(admin.ModelAdmin):
    list_display = ['name']

class ForecastAdmin(admin.ModelAdmin):
    list_display = ['user', 'match', 'team1_score','team2_score','score']
    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser:
            kwargs['exclude'] = ['user']
        return super(ForecastAdmin, self).get_form(request, obj, **kwargs)
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = request.user
        obj.save()
    def queryset(self, request):
        qs = super(ForecastAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Forecast, ForecastAdmin)
