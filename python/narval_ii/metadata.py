"""
NARVAL-II Metadata loader
"""

import os
import datetime
import itertools

import dateutil.tz as datetz
import yaml

import matplotlib

BASEDIR = os.path.abspath(os.path.dirname(__file__))
DATADIR = os.path.abspath(os.path.join(BASEDIR, '..', '..', 'metadata'))

def parse_flight_date(flight_date):
    """
    Convert a flight date (YYYYMMDD) to datetime object.
    """
    return datetime.datetime.strptime(str(flight_date), "%Y%m%d").replace(tzinfo=datetz.tzutc())

def parse_segment_time(segment_time):
    """
    Convert a segment time (HHMMSS) to timedelta object.
    """
    segment_time = str(segment_time)
    return datetime.timedelta(hours=int(segment_time[0:2]),
                              minutes=int(segment_time[2:4]),
                              seconds=int(segment_time[4:6]))

EXTRA_COLORS = {"rose": "#FF007F"}

def _add_colors():
    for cname, chex in EXTRA_COLORS.items():
        if cname not in matplotlib.colors.cnames:
            matplotlib.colors.cnames[cname] = chex

_add_colors()

class Color(object):
    def __init__(self, definition):
        self.definition = definition
    @property
    def rgb(self):
        return matplotlib.colors.colorConverter.to_rgb(self.definition)
    @property
    def html(self):
        return matplotlib.colors.rgb2hex(self.rgb)
    def __repr__(self):
        return "Color({})".format(repr(self.definition))

class Dropsonde(object):
    def __init__(self, ds_id):
        self.ds_id = ds_id
        try:
            date = datetime.datetime.strptime(self.ds_id, "D%Y%m%d_%H%M%S")
        except ValueError:
            raise ValueError("{} is an invalid dropsonde id!".format(ds_id))
        self.date = date.replace(tzinfo=datetz.tzutc())
    def __repr__(self):
        return "Dropsonde({})".format(repr(self.ds_id))

class Associateable(object):
    _containers = []
    def associate(self, key, objects):
        matching_objects = [obj for obj in objects if self.matches_date(obj.date)]
        setattr(self, key, matching_objects)
        for container_collection in self._containers:
            for container in getattr(self, container_collection):
                container.associate(key, matching_objects)

class Segment(Associateable):
    color = None
    def __init__(self, flight, name, start_time, end_time):
        self.flight = flight
        self.name = name
        self.start_time = start_time
        self.end_time = end_time

    @classmethod
    def from_dict(cls, flight, definition):
        start = flight.date + parse_segment_time(definition["times"][0])
        end = flight.date + parse_segment_time(definition["times"][1])
        new = cls(flight, definition["name"], start, end)
        new.color = Color(definition.get("color", None))
        return new

    def matches_date(self, date):
        return (date >= self.start_time) and (date <= self.end_time)

    def __repr__(self):
        return "<Segment {} of flight {}>".format(self.name, self.flight.name)

class Flight(Associateable):
    color = None
    _containers = ["segments"]
    def __init__(self, name, date):
        self.name = name
        self.date = date
        self.segments = []

    @classmethod
    def from_dict(cls, name, definition):
        date = parse_flight_date(definition["date"])
        new = cls(name, date)
        new.color = Color(definition.get("color", None))
        for segment in definition.get("segments", []):
            new.add_segment(Segment.from_dict(new, segment))
        return new

    def add_segment(self, segment):
        self.segments.append(segment)

    def matches_date(self, date):
        return (date >= self.date) and (date < (self.date + datetime.timedelta(hours=24)))

    def __repr__(self):
        return "<Flight {}, {}>".format(self.name, self.date)


def load_dropsondes():
    data = yaml.load(open(os.path.join(DATADIR, 'sondes.yaml')))
    return sorted(map(Dropsonde, data),
                  key=lambda sonde: sonde.date)


def load_flights():
    data = yaml.load(open(os.path.join(DATADIR, 'flights.yaml')))
    flights = sorted(itertools.starmap(Flight.from_dict, data.iteritems()),
                     key=lambda flight: flight.date)
    dropsondes = load_dropsondes()
    for flight in flights:
        flight.associate("dropsondes", dropsondes)
    return flights

def _main():
    for flight in load_flights():
        print(flight)
        print(flight.dropsondes)
        for segment in flight.segments:
            print("{0.name} ({0.color}) {0.start_time:%H:%M:%S}->{0.end_time:%H:%M:%S}".format(segment))
            print segment.dropsondes

if __name__ == '__main__':
    _main()
