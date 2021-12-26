import datetime
import io

from icalendar import Calendar, Event, Alarm

import dateutil


class RC3Talk():
    def __init__(self, title, description, start_date, end_date, room, track, language, speakers, join_url, schedule_url):
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.room = room
        self.track = track
        self.language = language
        self.speakers = speakers
        self.join_url = join_url
        self.schedule_url = schedule_url

    def get_ical_byte_list(self):
        time_zone = dateutil.tz.gettz('Europe / Berlin')

        cal = Calendar()

        cal.add('prodid', f'-//RC3 talk calendar//{self.title}//EN')
        cal.add('version', '2.0')

        event = Event()
        event.add('summary', self.title)
        event.add('dtstart', self.start_date)
        event.add('dtend', self.end_date)
        event.add('dtstamp', datetime.datetime.now(tz=time_zone))
        event.add('created', datetime.datetime.now(tz=time_zone))
        event.add('LOCATION', self.join_url)
        event.add('description', f"Schedule: {self.schedule_url}")

        alarm = Alarm()
        alarm.add('TRIGGER', datetime.timedelta(minutes=-5))
        alarm.add('ACTION', 'DISPLAY')
        alarm.add('DESCRIPTION', f'{self.title} starts in 5 minutes!')
        event.add_component(alarm)

        cal.add_component(event)

        arr = io.BytesIO(cal.to_ical())
        arr.seek(0)
        return arr
