from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime

class Tournament(models.Model):
    name = models.CharField(max_length=256, primary_key=True)
    def __unicode__(self):
        return u'%s' % (self.name,)

class Match(models.Model):
    class Meta:
        verbose_name_plural = 'Matches'
    tournament = models.ForeignKey('Tournament', blank=True, null=True)
    start = models.DateTimeField()
    location = models.CharField(max_length=1024, blank=True, null=True)
    team1 = models.ForeignKey('Team', related_name='matches1')
    team2 = models.ForeignKey('Team', related_name='matches2')
    team1_score = models.PositiveSmallIntegerField(blank=True, null=True)
    team2_score = models.PositiveSmallIntegerField(blank=True, null=True)
    def __unicode__(self):
        return u'%s : %s - %s' % (self.start.strftime('%Y-%m-%d %H:%M'), self.team1, self.team2) + '%s%s' % ((' (%s - ' % self.team1_score) if self.team1_score is not None else '', ('%s)' % self.team2_score) if self.team2_score is not None else '')
    def clean(self):
        if self.team1 == self.team2:
            raise ValidationError('Teams must be different.')
    def started(self):
        return datetime.datetime.now() >= self.start
    started.boolean = True

class Team(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    def __unicode__(self):
        return u'%s' % (self.name,)

class Forecast(models.Model):
    class Meta:
        unique_together = ('user', 'match')
    user = models.ForeignKey(User)
    match = models.ForeignKey("Match")
    team1_score = models.PositiveSmallIntegerField()
    team2_score = models.PositiveSmallIntegerField()
    def editable(self):
        return not self.match.started()
    editable.boolean = True
    def clean(self):
        try:
            if not self.editable():
                raise ValidationError('The match has already started.')
        except Match.DoesNotExist as e:
            pass
    def score(self):
	score = 0
        if None in (self.team1_score, self.team2_score, self.match.team1_score, self.match.team2_score):
            return score
	if self.team1_score == self.match.team1_score and self.team2_score == self.match.team2_score:
		score = score + 1
	if self.match.team1_score == self.match.team2_score and self.team1_score == self.team2_score:
		score = score + 1
	if self.match.team1_score > self.match.team2_score and self.team1_score > self.team2_score:
		score = score + 1
	if self.match.team1_score < self.match.team2_score and self.team1_score < self.team2_score:
		score = score + 1
	return score

