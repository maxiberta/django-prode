#!/usr/bin/env python

import urllib2
from BeautifulSoup import BeautifulSoup
from icalendar import Calendar, Event
from datetime import datetime
from icalendar import UTC # timezone
import dateutil.parser
import re

soup = BeautifulSoup(urllib2.urlopen('https://secure.wikimedia.org/wikipedia/es/wiki/Torneo_Apertura_2011_%28Argentina%29').read())
cal = Calendar()

for table in soup('table'):
    if table('tr')[0].th:
        if str(table('tr')[0].th.text).startswith('Fecha '):
            last_start = None
            for tr in table('tr')[2:]:
                event = Event()
                team1 = unicode(tr('td')[0].text)
                result = unicode(tr('td')[1].text)
                team2 = unicode(tr('td')[2].text)
                event.add('location', tr('td')[3].text)
                result_re = re.compile(r'^.*(\d+).*-.*(\d+).*$')
                r = result_re.match(result)
                if r:
                    team1_score = int(r.groups()[0])
                    team2_score = int(r.groups()[1])
                    event.add('summary', u'%s %d v %s %d' % (team1, team1_score, team2, team2_score))
                else:
                    event.add('summary', u'%s v %s' % (team1, team2))
                if len(tr('td')) == 6:
                    last_start = dateutil.parser.parse(tr('td')[4].text, fuzzy=True)
                if len(tr('td')) > 4:
                    try:
                        time = datetime.strptime(tr('td')[-1].text, '%H:%M')
                        start = datetime(last_start.year, last_start.month, last_start.day, time.hour, time.minute)
                        event.add('dtstart', start)
                    except ValueError:
                        pass
                cal.add_component(event)

print cal.as_string()
