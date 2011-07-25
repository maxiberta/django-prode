# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
import django_tables as tables
from django_prode.models import *

def index(request):
        class ScoreTable(tables.MemoryTable):
                class Meta:
                        sortable = False
		position = tables.Column()
                user = tables.Column()
		score = tables.Column()

	scores = []
	for user in User.objects.filter(is_superuser=False):
		scores.append({'user':user, 'score':sum([forecast.score() for forecast in Forecast.objects.filter(user=user)])})
	for row in enumerate(sorted(scores, key=lambda xxx: xxx['score'], reverse=True), 1):
		row[1]['position'] = row[0]

        table = ScoreTable(scores)
        return render_to_response('index.html', {"table":table}, context_instance=RequestContext(request))

