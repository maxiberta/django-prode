from django_prode.models import *
from django.contrib import admin
from django.forms.models import ModelForm
import datetime

class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name',]

class MatchAdmin(admin.ModelAdmin):
    list_display = ['tournament', '__unicode__', 'start', 'location', 'started']
    list_filter = ['tournament']

class TeamAdmin(admin.ModelAdmin):
    list_display = ['name']

class ForecastAdmin(admin.ModelAdmin):
    list_display = ['user', 'match', 'team1_score', 'team2_score', 'score', 'editable']
    def forecast_form_factory(self, user):
        class ForecastForm(ModelForm):
            class Meta:
                model = Forecast
            def __init__(self, *args, **kwargs):
                super(ForecastForm, self).__init__(*args, **kwargs)
                self.fields['match'].queryset = Match.objects.filter(start__gt=datetime.datetime.now()).exclude(forecast__user=user)
        return ForecastForm
    def get_form(self, request, obj=None, **kwargs):
        self.form = self.forecast_form_factory(request.user)
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
