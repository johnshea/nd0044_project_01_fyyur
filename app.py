#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import datetime
from models import db, Artist, Venue, Show, Genre

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  value = str(value)
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

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
  data = []
  locations = db.session.query(Venue.state, Venue.city).order_by(Venue.state, Venue.city).distinct().all()
  for location in locations:
    venues = db.session.query(Venue.id, Venue.name).order_by(Venue.name).filter(Venue.state==location.state, Venue.city==location.city).all()
    data_city = location._asdict()
    data_city['venues'] = [venue._asdict() for venue in venues]
    data.append(data_city)

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # Search on venues' name with partial case-insensitive string search.
  results = db.session.query(Venue.id, Venue.name).order_by(Venue.name).filter(Venue.name.ilike('%'+request.form.get('search_term', '')+'%')).all()
  
  response = {
    "count": len(results),
    "data": results
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  data_venue = Venue.query.get(venue_id)
  if not data_venue:
    abort(404)

  shows_query = db.session \
    .query(Artist.id.label('artist_id'),Artist.name.label('artist_name'),Artist.image_link.label('artist_image_link'),Show.start_time) \
    .join(Show) \
    .join(Venue) \
    .filter(Venue.id==venue_id) \
    .order_by(Show.start_time)
  
  data_past_shows = shows_query.filter(Show.start_time < datetime.datetime.now()).all()

  data_upcoming_shows = shows_query.filter(Show.start_time >= datetime.datetime.now()).all()

  data_genres = []
  for genre in data_venue.genres:
    data_genres.append(genre.name)

  data = {
    "id": data_venue.id,
    "name": data_venue.name,
    "genres": data_genres,
    "address": data_venue.address,
    "city": data_venue.city,
    "state": data_venue.state,
    "phone": data_venue.phone,
    "website": data_venue.website,
    "facebook_link": data_venue.facebook_link,
    "seeking_talent": data_venue.seeking_talent,
    "image_link": data_venue.image_link,
    "past_shows": data_past_shows,
    "upcoming_shows": data_upcoming_shows,
    "past_shows_count": len(data_past_shows),
    "upcoming_shows_count": len(data_upcoming_shows),
  }

  if data_venue.seeking_talent:
    data['seeking_description'] = data_venue.seeking_description
  else:
    data['seeking_description'] = ''

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

  try:

    form = VenueForm(meta={'csrf': False})

    if not form.validate():
      raise Exception('Form field failed validation')

    data = request.form
    new_venue = Venue()

    if data.get('name'):
      new_venue.name = data.get('name')

    if data.get('city'):
      new_venue.city = data.get('city')

    if data.get('state'):
      new_venue.state = data.get('state')

    if data.get('address'):
      new_venue.address = data.get('address')

    if data.get('phone'):
      new_venue.phone = data.get('phone')

    if data.get('image_link'):
      new_venue.image_link = data.get('image_link')

    if data.get('facebook_link'):
      new_venue.facebook_link = data.get('facebook_link')

    if data.get('seeking_talent'):
      new_venue.seeking_talent = True

    if data.get('seeking_description'):
      new_venue.seeking_description = data.get('seeking_description')

    if data.getlist('genres'):
      for item in data.getlist('genres'):
        new_genre = Genre.query.filter(Genre.name==item).first()
        if new_genre:
          new_venue.genres.append(new_genre)

    if data.get('website_link'):
      new_venue.website = data.get('website_link')
  
    db.session.add(new_venue)
    db.session.commit()

    # on successful db insert, flash success
    flash('Venue "' + request.form['name'] + '" was successfully listed!', 'alert-success')

  except Exception as e:
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue "' + request.form['name'] + '" could not be listed.', 'alert-danger')
    db.session.rollback()
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  venue = Venue.query.get(venue_id)

  if not venue:
    abort(404)

  try:
    db.session.delete(venue)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.with_entities(Artist.id, Artist.name).all()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # Search on artists' name with partial case-insensitive string search.
  results = db.session.query(Artist.id, Artist.name).order_by(Artist.name).filter(Artist.name.ilike('%'+request.form.get('search_term', '')+'%')).all()

  response = {
    "count": len(results),
    "data": results
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  data_artist = Artist.query.get(artist_id)
  if not data_artist:
    abort(404)

  data_past_shows = db.session.query(Venue.id.label('venue_id'),Venue.name.label('venue_name'),Venue.image_link.label('venue_image_link'),Show.start_time).filter(Venue.id==Show.venue_id).filter(Show.artist_id==Artist.id).filter(Artist.id==artist_id).filter(Show.start_time < datetime.datetime.now()).all()
  data_upcoming_shows = db.session.query(Venue.id.label('venue_id'),Venue.name.label('venue_name'),Venue.image_link.label('venue_image_link'),Show.start_time).filter(Venue.id==Show.venue_id).filter(Show.artist_id==Artist.id).filter(Artist.id==artist_id).filter(Show.start_time >= datetime.datetime.now()).all()

  data_genres = []
  for genre in data_artist.genres:
    data_genres.append(genre.name)

  data = {
    "id": data_artist.id,
    "name": data_artist.name,
    "genres": data_genres,
    "city": data_artist.city,
    "state": data_artist.state,
    "phone": data_artist.phone,
    "website": data_artist.website,
    "facebook_link": data_artist.facebook_link,
    "seeking_venue": data_artist.seeking_venue,
    "image_link": data_artist.image_link,
    "past_shows": data_past_shows,
    "upcoming_shows": data_upcoming_shows,
    "past_shows_count": len(data_past_shows),
    "upcoming_shows_count": len(data_upcoming_shows),
  }

  if data_artist.seeking_venue:
    data['seeking_description'] = data_artist.seeking_description
  else:
    data['seeking_description'] = ''

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  data_artist = Artist.query.get(artist_id)

  if not data_artist:
    abort(404)

  form = ArtistForm(obj=data_artist)
  
  artist = {
    "id": data_artist.id,
    "name": data_artist.name
  }  

  data_genres = []
  for genre in data_artist.genres:
    data_genres.append(genre.name)

  if data_genres:
    form.genres.data = data_genres

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  artist = Artist.query.get(artist_id)

  if not artist:
    abort(404)

  try:
    form = ArtistForm(obj=artist, meta={'csrf': False})

    if not form.validate():
      raise Exception('Form field failed validation')

    artist.name = form.name.data

    artist.city = form.city.data

    artist.state = form.state.data

    artist.phone = form.phone.data

    artist.image_link = form.image_link.data

    artist.facebook_link = form.facebook_link.data

    artist.seeking_venue = form.seeking_venue.data

    artist.seeking_description = form.seeking_description.data

    new_genre_list = []
    if form.genres.data:
      for item in form.genres.data:
        new_genre = Genre.query.filter(Genre.name==item).first()
        if new_genre:
          new_genre_list.append(new_genre)
    
    artist.genres = new_genre_list

    artist.website = form.website_link.data

    db.session.commit()

    # on successful db update, flash success
    flash('Artist "' + request.form['name'] + '" was successfully updated!', 'alert-success')

  except Exception as e:
    db.session.rollback()

    # on unsuccessful db update, flash an error instead.
    flash('An error occurred. Artist "' + request.form['name'] + '" could not be updated.', 'alert-danger')
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  data_venue = Venue.query.get(venue_id)

  if not data_venue:
    abort(404)

  form = VenueForm(obj=data_venue)

  venue = {
    "id": data_venue.id,
    "name": data_venue.name
  }  

  data_genres = []
  for genre in data_venue.genres:
    data_genres.append(genre.name)

  if data_genres:
    form.genres.data = data_genres

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  venue = Venue.query.get(venue_id)

  if not venue:
    abort(404)

  try:
    form = VenueForm(obj=venue, meta={'csrf': False})

    if not form.validate():
      raise Exception('Form field failed validation')

    venue.name = form.name.data

    venue.city = form.city.data

    venue.state = form.state.data

    venue.address = form.address.data

    venue.phone = form.phone.data

    venue.image_link = form.image_link.data

    venue.facebook_link = form.facebook_link.data

    venue.seeking_talent = form.seeking_talent.data

    venue.seeking_description = form.seeking_description.data

    new_genre_list = []
    if form.genres.data:
      for item in form.genres.data:
        new_genre = Genre.query.filter(Genre.name==item).first()
        if new_genre:
          new_genre_list.append(new_genre)
    
    venue.genres = new_genre_list

    venue.website = form.website_link.data

    db.session.commit()

    # on successful db update, flash success
    flash('Venue "' + request.form['name'] + '" was successfully updated!', 'alert-success')

  except:
    db.session.rollback()

    # on unsuccessful db update, flash an error instead.
    flash('An error occurred. Venue "' + request.form['name'] + '" could not be updated.', 'alert-danger')
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form

  try:

    form = ArtistForm(meta={'csrf': False})

    if not form.validate():
      raise Exception('Form field failed validation')

    new_artist = Artist()

    new_artist.name = form.name.data

    new_artist.city = form.city.data

    new_artist.state = form.state.data

    new_artist.phone = form.phone.data

    new_artist.image_link = form.image_link.data

    new_artist.facebook_link = form.facebook_link.data

    new_artist.seeking_venue = form.seeking_venue.data

    new_artist.seeking_description = form.seeking_description.data

    if form.genres.data:
      for item in form.genres.data:
        new_genre = Genre.query.filter(Genre.name==item).first()
        if new_genre:
          new_artist.genres.append(new_genre)

    new_artist.website = form.website_link.data
  
    db.session.add(new_artist)
    db.session.commit()

    # on successful db insert, flash success
    flash('Artist "' + request.form['name'] + '" was successfully listed!', 'alert-success')

  except:
    db.session.rollback()

    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist "' + request.form['name'] + '" could not be listed.', 'alert-danger')
  finally:
    db.session.close()

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  data = db.session.query(Venue.id.label('venue_id'), Venue.name.label('venue_name'), Artist.id.label('artist_id'), Artist.name.label('artist_name'), Artist.image_link.label('artist_image_link'), Show.start_time.label('start_time')).filter(Venue.id==Show.venue_id).filter(Show.artist_id==Artist.id).order_by(Show.start_time).all()
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  try:

    form = ShowForm(meta={'csrf': False})

    if not form.validate():
      raise Exception('Form field failed validation')

    new_show = Show()

    new_show.artist_id = form.artist_id.data

    new_show.venue_id = form.venue_id.data

    new_show.start_time = form.start_time.data

    db.session.add(new_show)
    db.session.commit()

    # on successful db insert, flash success
    flash('Show was successfully listed!', 'alert-success')

  except:
    db.session.rollback()

    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be listed.', 'alert-danger')
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
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
