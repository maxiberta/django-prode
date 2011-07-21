from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from icalendar import Calendar
import re
from fixture.models import *

class Command(BaseCommand):
    args = '<icalendar icalendar ...>'
    help = 'Imports tournament events from iCal'

    option_list = BaseCommand.option_list + (
        make_option('-t', '--tournament',
            dest='tournament',
            help='Associate matches to given tournament'),
    )

    def handle(self, *args, **options):
        for ical_filename in args:
            try:
                ical_string = file(ical_filename).read()
                cal = Calendar.from_string(ical_string.decode('iso8859-1').encode('utf8'))
                for component in cal.walk():
                    if component.name == "VEVENT":
                        summary = component.decoded('summary')
                        start = component.decoded('dtstart')
                        location = component.decoded('location')
                        tournament = options['tournament']
                        r_compiled = re.compile(r'^(?P<team1>[A-z\. ]+)(?P<team1_score>[0-9]*) v[s\.]* (?P<team2>[A-z\. ]+)(?P<team2_score>[0-9]*) .*$')
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
                        try:
                            tournament_instance = Tournament.objects.get(name=tournament)
                        except Tournament.DoesNotExist as e:
                            tournament_instance = Tournament.objects.create(name=tournament)
                        match = Match(tournament=tournament_instance, start=start, location=location, team1=team1_instance, team2=team2_instance, team1_score=team1_score, team2_score=team2_score)
                        if Match.objects.filter(team1=team1_instance, team2=team2_instance, start__year=start.year, start__month=start.month, start__day=start.day).exists() or Match.objects.filter(team1=team2_instance, team2=team1_instance, start__year=start.year, start__month=start.month, start__day=start.day).exists():
                            self.stdout.write('Found previous instance of "%s". Not importing!\n' % match)
                            continue
                        match.save()

            except Exception as e:
                raise CommandError(e)
        self.stdout.write('Successfully imported calendar\n')

