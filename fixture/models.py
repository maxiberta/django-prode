from django.db import models

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
    team1_score = models.SmallIntegerField(blank=True, null=True)
    team2_score = models.SmallIntegerField(blank=True, null=True)
    def __unicode__(self):
        return u'%s - %s' % (self.team1, self.team2) + '%s%s' % ((' (%s - ' % self.team1_score) if self.team1_score is not None else '', ('%s)' % self.team2_score) if self.team2_score is not None else '')

class Team(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    def __unicode__(self):
        return u'%s' % (self.name,)
