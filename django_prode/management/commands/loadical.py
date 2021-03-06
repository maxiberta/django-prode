# coding=utf-8

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from icalendar import Calendar
import re
from django_prode.models import *

class Command(BaseCommand):
    args = '<icalendar icalendar ...>'
    help = 'Imports tournament events from iCal'

    option_list = BaseCommand.option_list + (
        make_option('-t', '--tournament',
            dest='tournament',
            help='Associate matches to given tournament'),
    )

    def handle(self, *args, **options):
        files = map(lambda x: open(x, 'r'), args)
        if len(args) == 0:
            import sys
            files.append(sys.stdin)
        for ical_file in files:
            try:
                ical_string = ical_file.read()
                cal = Calendar.from_string(ical_string)
                for component in cal.walk():
                    if component.name == "VEVENT":
                        summary = component.decoded('summary')
                        try:
                            start = component.decoded('dtstart')
                        except:
                            start = None
                        location = component.decoded('location')
                        tournament = options['tournament']
                        r_compiled = re.compile(u'^(?P<team1>[A-záéíóú´\'\(\)\. ]+)(?P<team1_score>[0-9]*) v[s\.]* (?P<team2>[A-záéíóú´\'\(\)\. ]+)(?P<team2_score>[0-9]*).*$')
                        r = r_compiled.match(summary)
                        team1 = r.group('team1').strip()
                        team2 = r.group('team2').strip()
                        team1_score = r.group('team1_score').strip() or None
                        team2_score = r.group('team2_score').strip() or None
                        try:
                            team1_instance = Team.objects.get(name=team1)
                        except Team.DoesNotExist as e:
                            team1_instance = Team.objects.create(name=team1)
                        try:
                            team2_instance = Team.objects.get(name=team2)
                        except Team.DoesNotExist as e:
                            team2_instance = Team.objects.create(name=team2)
                        if tournament:
                            try:
                                tournament_instance = Tournament.objects.get(name=tournament)
                            except Tournament.DoesNotExist as e:
                                tournament_instance = Tournament.objects.create(name=tournament)
                        else:
                            tournament_instance = None
                        match = Match(tournament=tournament_instance, start=start, location=location, team1=team1_instance, team2=team2_instance, team1_score=team1_score, team2_score=team2_score)
                        if start:
                            if Match.objects.filter(team1=team1_instance, team2=team2_instance, start__year=start.year, start__month=start.month, start__day=start.day).exists() or Match.objects.filter(team1=team2_instance, team2=team1_instance, start__year=start.year, start__month=start.month, start__day=start.day).exists():
                                self.stdout.write(u'Found previous instance of "%s". Not importing!\n' % match)
                                continue
                        match.save()

            except Exception as e:
                raise CommandError(e)
        self.stdout.write(u'Successfully imported calendar\n')

