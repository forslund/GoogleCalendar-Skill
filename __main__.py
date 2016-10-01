import sys
import os
import httplib2
from googleapiclient import discovery
import datetime as dt
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
get_credentials = __import__('GoogleCalendar-Skill').get_credentials


"""Handles basic authentication and provides feedback in form of upcoming
   events (if any) after completion.
"""

sys.argv.append('--noauth_local_webserver')
credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('calendar', 'v3', http=http)

now = dt.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
print('Getting the upcoming 10 events')
eventsResult = service.events().list(
    calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
    orderBy='startTime').execute()
events = eventsResult.get('items', [])

if not events:
    print('No upcoming events found.')
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    d = dt.datetime.strptime(start[:-6], '%Y-%m-%dT%H:%M:%S')
    starttime = dt.datetime.strftime(d, '%H %M')
    print(event['summary'] + ' at ' + starttime)
