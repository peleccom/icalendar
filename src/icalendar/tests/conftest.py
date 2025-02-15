import os
import logging
import pytest
import icalendar
import pytz
from datetime import datetime
from dateutil import tz
try:
    import zoneinfo
except ModuleNotFoundError:
    from backports import zoneinfo


class DataSource:
    '''A collection of parsed ICS elements (e.g calendars, timezones, events)'''
    def __init__(self, data_source_folder, parser):
        self._parser = parser
        self._data_source_folder = data_source_folder

    def __getattr__(self, attribute):
        """Parse a file and return the result stored in the attribute."""
        source_file = attribute.replace('-', '_') + '.ics'
        source_path = os.path.join(self._data_source_folder, source_file)
        with open(source_path, 'rb') as f:
            raw_ics = f.read()
        source = self._parser(raw_ics)
        source.raw_ics = raw_ics
        self.__dict__[attribute] = source
        return source

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return repr(self.__dict__)

HERE = os.path.dirname(__file__)
TIMEZONES_FOLDER = os.path.join(HERE, 'timezones')
EVENTS_FOLDER = os.path.join(HERE, 'events')
CALENDARS_FOLDER = os.path.join(HERE, 'calendars')

@pytest.fixture
def timezones():
    return DataSource(TIMEZONES_FOLDER, icalendar.Timezone.from_ical)

@pytest.fixture
def events():
    return DataSource(EVENTS_FOLDER, icalendar.Event.from_ical)

@pytest.fixture(params=[
    pytz.utc,
    zoneinfo.ZoneInfo('UTC'),
    pytz.timezone('UTC'),
    tz.UTC,
    tz.gettz('UTC')])
def utc(request):
    return request.param

@pytest.fixture
def calendars():
    return DataSource(CALENDARS_FOLDER, icalendar.Calendar.from_ical)
