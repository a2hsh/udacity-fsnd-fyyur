# This file contains all models of the database, and their helper functions

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Declaring models


class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(150))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(
        db.Boolean, nullable=False, default=False, server_default='false')
    seeking_description = db.Column(db.String(500))
    availability = db.relationship(
        'ArtistAvailability', backref='artists', lazy=True, cascade='all, delete-orphan', passive_deletes=True)
    venues = db.relationship('Venue', secondary='shows',
                             backref='artists', lazy=True)
    shows = db.relationship('Show', backref='artists',
                            lazy=True, cascade='all, delete-orphan', passive_deletes=True)


class ArtistAvailability(db.Model):
    __tablename__ = 'artist_availability'
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id', ondelete='CASCADE'), primary_key=True, nullable=False)
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


class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(150))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(
        db.Boolean, nullable=False, default=False, server_default='false')
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='venues',
                            lazy=True, cascade='all, delete-orphan', passive_deletes=True)


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id', ondelete='CASCADE'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venues.id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
