from django.test import TestCase
from django_prode.models import *
from django.contrib.auth.models import User
import datetime

class ForecastTest(TestCase):
    def setUp(self):
        '''Set up a couple of matches with different results'''
        self.user = User.objects.create_user('user1', 'user1@example.com')
        team1 = Team.objects.create(name='Team1')
        team2 = Team.objects.create(name='Team2')
        self.tie = Match.objects.create(team1=team1, team2=team2, team1_score=0, team2_score=0, start=datetime.datetime.now() + datetime.timedelta(1))
        self.team1_wins = Match.objects.create(team1=team1, team2=team2, team1_score=1, team2_score=0, start=datetime.datetime.now() + datetime.timedelta(2))
        self.team2_wins = Match.objects.create(team1=team1, team2=team2, team1_score=0, team2_score=1, start=datetime.datetime.now() + datetime.timedelta(3))
        self.not_yet_played = Match.objects.create(team1=team1, team2=team2, start=datetime.datetime.now() + datetime.timedelta(4))

    def test_tie_score(self):
        '''Set up a couple forecasts and verify user scores on tie'''
        forecast = Forecast(user=self.user, match=self.tie, team1_score=self.tie.team1_score, team2_score=self.tie.team2_score)
        self.assertEquals(forecast.score(), 2)
        forecast.team1_score = self.tie.team1_score + 1
        forecast.team2_score = self.tie.team2_score + 1
        self.assertEquals(forecast.score(), 1)
        forecast.team1_score = forecast.team1_score + 1
        self.assertEquals(forecast.score(), 0)
        forecast.team2_score = forecast.team1_score + 1
        self.assertEquals(forecast.score(), 0)

    def test_team1_wins_score(self):
        '''Set up a couple forecasts and verify user scores on team1 win'''
        forecast = Forecast(user=self.user, match=self.team1_wins, team1_score=self.team1_wins.team1_score, team2_score=self.team1_wins.team2_score)
        self.assertEquals(forecast.score(), 2)
        forecast.team1_score = self.team1_wins.team1_score + 1
        forecast.team2_score = self.team1_wins.team2_score + 1
        self.assertEquals(forecast.score(), 1)
        forecast.team1_score = 0
        forecast.team2_score = 1
        self.assertEquals(forecast.score(), 0)
        forecast.team2_score = forecast.team1_score
        self.assertEquals(forecast.score(), 0)

    def test_team2_wins_score(self):
        '''Set up a couple forecasts and verify user scores on team2 win'''
        forecast = Forecast(user=self.user, match=self.team2_wins, team1_score=self.team2_wins.team1_score, team2_score=self.team2_wins.team2_score)
        self.assertEquals(forecast.score(), 2)
        forecast.team1_score = self.team2_wins.team1_score + 1
        forecast.team2_score = self.team2_wins.team2_score + 1
        self.assertEquals(forecast.score(), 1)
        forecast.team1_score = 1
        forecast.team2_score = 0
        self.assertEquals(forecast.score(), 0)
        forecast.team2_score = forecast.team1_score
        self.assertEquals(forecast.score(), 0)

    def test_not_yet_played_score(self):
        '''Verify no score is assigned before the match is actually played'''
        forecast = Forecast(user=self.user, match=self.not_yet_played, team1_score=None, team2_score=None)
        self.assertEquals(forecast.score(), 0)
        forecast.team1_score = 0
        forecast.team2_score = 0
        self.assertEquals(forecast.score(), 0)

