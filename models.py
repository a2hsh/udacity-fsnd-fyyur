# This file contains all models of the database, and their helper functions

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()

# Declaring models


class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(150), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(
        db.Boolean, nullable=False, default=False, server_default='false')
    seeking_description = db.Column(db.String(500))
    monday = db.Column(db.Boolean, nullable=False,
                       default=True, server_default='true')
    tuesday = db.Column(db.Boolean, nullable=False,
                        default=True, server_default='true')
    wednesday = db.Column(db.Boolean, nullable=False,
                          default=True, server_default='true')
    thursday = db.Column(db.Boolean, nullable=False,
                         default=True, server_default='true')
    friday = db.Column(db.Boolean, nullable=False,
                       default=True, server_default='true')
    saturday = db.Column(db.Boolean, nullable=False,
                         default=True, server_default='true')
    sunday = db.Column(db.Boolean, nullable=False,
                       default=True, server_default='true')
    venues = db.relationship('Venue', secondary='shows',
                             backref='artist', lazy=True)
    shows = db.relationship('Show', backref='artist',
                            lazy=True, cascade='all, delete-orphan', passive_deletes=True)

    # query shows table for number of past shows for the given artist
    @hybrid_property
    def past_shows_count(self):
        return len(list(filter(lambda x: x.start_time < datetime.today(), self.shows)))

    # query shows table for number of upcomming shows for the given artist
    @hybrid_property
    def upcoming_shows_count(self):
        return len(list(filter(lambda x: x.start_time > datetime.today(), self.shows)))

    # query artists table for availability on weekdays, returning a string to frontEnd
    @hybrid_property
    def availability(self):
        weekDays = ['monday', 'tuesday', 'wednesday',
                    'thursday', 'friday', 'saturday', 'sunday']
        daylist = []
        for day in weekDays:
            if getattr(self, day):
                daylist.append(day)
        if not daylist:
            return f'but haven\'t specified weekly availability dates. Please contact {self.name} for more details.'
        elif daylist == weekDays:
            return 'all week!'
        daylist.insert(-1, 'and')
        return 'on ' + ', '.join(daylist[:-2]) + ' ' + ' '.join(daylist[-2:])

    # returns a dictionary for the given artist
    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'genres': self.genres.split(),  # convert string to list
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'availability': self.availability,
            'upcoming_shows_count': self.upcoming_shows_count,
            'past_shows_count': self.past_shows_count
        }

    # Check availability for validation on shows form, returns a tuple of true / false, and the specified date in the form to the frontEnd
    def availableOn(self, date):
        weekDays = ('monday', 'tuesday', 'wednesday',
                    'thursday', 'friday', 'saturday', 'sunday')
        weekDate = date.weekday()
        weekDateStr = weekDays[weekDate]
        checkDate = getattr(self, weekDateStr)
        if checkDate:
            return True, weekDateStr
        else:
            return False, weekDateStr


class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(150), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(
        db.Boolean, nullable=False, default=False, server_default='false')
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='venue',
                            lazy=True, cascade='all, delete-orphan', passive_deletes=True)

    @hybrid_property
    def past_shows_count(self):
        return len(list(filter(lambda x: x.start_time < datetime.today(), self.shows)))

    @hybrid_property
    def upcoming_shows_count(self):
        return len(list(filter(lambda x: x.start_time > datetime.today(), self.shows)))

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'address': self.address,
            'genres': self.genres.split(),
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'upcoming_shows_count': self.upcoming_shows_count,
            'past_shows_count': self.past_shows_count
        }


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id', ondelete='CASCADE'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venues.id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    def venueDict(self):
        return {
            'venue_id': self.venue.id,
            'venue_name': self.venue.name,
            'venue_image_link': self.venue.image_link,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M')
        }

    def artistDict(self):
        return {
            'artist_id': self.artist.id,
            'artist_name': self.artist.name,
            'artist_image_link': self.artist.image_link,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M')
        }
