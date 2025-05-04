
import requests
import time
from threading import Thread
import datetime
from ics import Calendar

class CalendarSync(Thread):
    def __init__(self, runtime, ics_url):
        super().__init__(daemon=True)
        self.runtime = runtime
        self.ics_url = ics_url

    def run(self):
        while True:
            try:
                r = requests.get(self.ics_url)
                cal = Calendar(r.text)
                now = datetime.datetime.now()
                today_events = [e for e in cal.events if now.date() == e.begin.date()]
                self.runtime.memory.add({"sensor": "calendar", "events": [e.name for e in today_events]})
            except:
    print('Calendar fallback')
