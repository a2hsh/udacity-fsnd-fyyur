#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_migrate import Migrate
from models import db, Venue, Artist, Show
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_wtf.csrf import CSRFProtect
from forms import *
import sys
from itertools import groupby
from sqlalchemy import or_

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

csrf = CSRFProtect()
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
csrf.init_app(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # query all venues and order results by state and city.
    venues = Venue.query.order_by(Venue.state, Venue.city).all()
    data = []
    # group venues by city and state, storing them in dictionaries.
    for key, group in groupby(venues, lambda x: (x.city, x.state)):
        dict = {
            'city': key[0],
            'state': key[1],
            'venues': list(group)
        }
        data.append(dict)
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # filter venue names, cities, states, and genres by search term
    venues = Venue.query.filter(or_(Venue.name.ilike('%' + request.form.get('search_term') + '%'), Venue.city.ilike('%' + request.form.get('search_term') + '%'),
                                    Venue.state.ilike('%' + request.form.get('search_term') + '%'), Venue.genres.ilike('%' + request.form.get('search_term') + '%')))
    data = []
    [data.append(venue.dict()) for venue in venues]
    response = {}
    response['count'] = len(data)
    response['data'] = data
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    # shows the venue page with the given venue_id
    data = venue.dict()
    past_shows = list(filter(lambda x: x.start_time <
                             datetime.today(), venue.shows))
    upcoming_shows = list(filter(lambda x: x.start_time >
                                 datetime.today(), venue.shows))
    past_shows = list(map(lambda x: x.artistDict(), past_shows))
    upcoming_shows = list(map(lambda x: x.artistDict(), upcoming_shows))
    data['past_shows'] = past_shows
    data['upcoming_shows'] = upcoming_shows
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET', 'POST'])
def create_venue_submission():
    form = VenueForm()
    error = False
    # if the form passed validation, populate the venue object from form data
    if form.validate_on_submit():
        try:
            venue = Venue()

            form.populate_obj(venue)
            # genres is a list, so convert it to string
            genresList = request.form.getlist('genres')
            venue.genres = ', '.join(genresList)
            db.session.add(venue)
            # to return users to the new venue's page, flush the session, and store the id in another variable
            db.session.flush()
            venue_id = venue.id
            db.session.commit()
        except:
            # if failed, roll back and display a message to the user
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
            # if error, return to home and display a message, or go to the new venue's page
            if error:
                flash('Oops! Something wrong happened, venue ' +
                      str(form.name.data) + ' could not be listed!', 'error')
                return render_template('pages/home.html')
            else:
                flash(
                    'Venue ' + str(form.name.data) + ' was listed successfully!')
                return redirect(url_for('show_venue', venue_id=venue_id))
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    error = False
    try:
        venue = Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash('Oops! Something wrong happened, venue ' +
                  venue.name + ' could not be deleted.', 'error')
        else:
            flash('venue ' +
                  venue.name + ' was deleted successfully.')
    return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # query all artists, ordered by names.
    data = Artist.query.order_by(Artist.name).all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # filter artist names, cities, states, and genres by search term
    artists = Artist.query.filter(or_(Artist.name.ilike('%' + request.form.get('search_term') + '%'), Artist.city.ilike('%' + request.form.get('search_term') + '%'),
                                      Artist.state.ilike('%' + request.form.get('search_term') + '%'), Artist.genres.ilike('%' + request.form.get('search_term') + '%')))
    data = []
    [data.append(artist.dict()) for artist in artists]
    response = {}
    response['count'] = len(data)
    response['data'] = data
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # query artist_id from db
    artist = Artist.query.get(artist_id)
    data = artist.dict()
    # filter shows based on current date
    past_shows = list(filter(lambda x: x.start_time <
                             datetime.today(), artist.shows))
    upcoming_shows = list(filter(lambda x: x.start_time >
                                 datetime.today(), artist.shows))
    # map venue information to shows
    past_shows = list(map(lambda x: x.venueDict(), past_shows))
    upcoming_shows = list(map(lambda x: x.venueDict(), upcoming_shows))
    data['past_shows'] = past_shows
    data['upcoming_shows'] = upcoming_shows
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET', 'POST'])
def edit_artist_submission(artist_id):
    # query artist_id from db
    artist = Artist.query.get(artist_id)
    # pass the artist object to form for editing
    form = ArtistForm(obj=artist)
    error = False
    # convert genres back to list, and append to form
    form.genres.data = artist.genres.split(', ')
    # if form passed validation, populate the artist object with form data
    if form.validate_on_submit():
        try:
            form.populate_obj(artist)
            genresList = request.form.getlist('genres')
            artist.genres = ', '.join(genresList)
            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
            if error:
                flash('Oops! Something wrong happened, artist' +
                      str(form.name.data) + ' could not be edited!', 'error')
            else:
                flash(
                    'Artist ' + request.form['name'] + ' was edited successfully!')
            return redirect(url_for('show_artist', artist_id=artist_id))
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/venues/<int:venue_id>/edit', methods=['GET', 'POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)
    error = False
    form.genres.data = venue.genres.split(', ')
    if form.validate_on_submit():
        try:
            form.populate_obj(venue)
            genresList = request.form.getlist('genres')
            venue.genres = ', '.join(genresList)
            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
            if error:
                flash('Oops! Something wrong happened, venue' +
                      str(form.name.data) + ' could not be edited!', 'error')
            else:
                flash(
                    'Venue ' + request.form['name'] + ' was edited successfully!')
            return redirect(url_for('show_venue', venue_id=venue_id))
    return render_template('forms/edit_venue.html', form=form, venue=venue)

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET', 'POST'])
def create_artist_submission():
    form = ArtistForm()
    error = False
    if form.validate_on_submit():
        try:
            artist = Artist()
            form.populate_obj(artist)
            genresList = request.form.getlist('genres')
            artist.genres = ', '.join(genresList)
            db.session.add(artist)
            # to return users to the new artist page, flush the session, and store the id in another variable
            db.session.flush()
            artist_id = artist.id
            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
            if error:
                flash('Oops! Something wrong happened, artist' +
                      str(form.name.data) + ' could not be listed!', 'error')
                return render_template('pages/home.html')
            else:
                flash(
                    'Artist ' + str(form.name.data) + ' was listed successfully!')
                return redirect(url_for('show_artist', artist_id=artist_id))
    return render_template('forms/new_artist.html', form=form)

#  Shows
#  ----------------------------------------------------------------


@app.route('/shows')
def shows():
    # displays list of shows at /shows
    data = []
    shows = Show.query.all()
    for show in shows:
        data.append({
            'venue_id': show.venue_id,
            'venue_name': show.venue.name,
            'artist_id': show.artist_id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.start_time.isoformat()
        })
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create', methods=['GET', 'POST'])
def create_show_submission():
    form = ShowForm()
    error = False
    # query only artists who seak venues
    artists = Artist.query.with_entities(
        Artist.id, Artist.name, Artist.seeking_venue).filter_by(seeking_venue=True)
    # query only venues who seak talent
    venues = Venue.query.with_entities(
        Venue.id, Venue.name, Venue.seeking_talent).filter_by(seeking_talent=True).all()
    artists_list = [(artist.id, artist.name) for artist in artists]
    venues_list = [(venue.id, venue.name) for venue in venues]
    form.artist_id.choices = artists_list
    form.venue_id.choices = venues_list
    if form.validate_on_submit():
        try:
            show = Show()
            form.populate_obj(show)
            db.session.add(show)
            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
            if error:
                flash(
                    'Oops! Something wrong happened, your show could not be listed!', 'error')
            else:
                flash(
                    'Your show was listed successfully!')
            return render_template('pages/home.html')
    return render_template('forms/new_show.html', form=form)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
