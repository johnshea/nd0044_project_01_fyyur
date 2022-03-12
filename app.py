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

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
      return f'<Show id={self.id}, venue_id={self.venue_id}, artist_id={self.artist_id}, start_time=\'{self.start_time}\'>'

venue_genre_association = db.Table("venue_genre_association",
    db.Column("venue_id", db.Integer, db.ForeignKey("venues.id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.id"), primary_key=True)
)

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String())
    genres = db.relationship("Genre", secondary=venue_genre_association, backref=db.backref("venues", lazy=True))
    website = db.Column(db.String(120))

    def __repr__(self):
      return f'<Venue id={self.id}, name=\'{self.name}\'>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

artist_genre_association = db.Table("artist_genre_association",
    db.Column("artist_id", db.Integer, db.ForeignKey("artists.id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.id"), primary_key=True)
)

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.relationship("Genre", secondary=artist_genre_association, backref=db.backref("artists", lazy=True))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String())
    website = db.Column(db.String(120))

    def __repr__(self):
      return f'<Artist id={self.id}, name=\'{self.name}\'>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Genre(db.Model):
    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)

    def __repr__(self):
      return f'<Genre id={self.id}, name=\'{self.name}\'>'

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

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
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  data_venue = Venue.query.get(venue_id)
  if not data_venue:
    abort(404)

  data_past_shows = db.session.query(Artist.id.label('artist_id'),Artist.name.label('artist_name'),Artist.image_link.label('artist_image_link'),Show.start_time).filter(Venue.id==Show.venue_id).filter(Show.artist_id==Artist.id).filter(Venue.id==venue_id).filter(Show.start_time < datetime.datetime.now()).all()
  data_upcoming_shows = db.session.query(Artist.id.label('artist_id'),Artist.name.label('artist_name'),Artist.image_link.label('artist_image_link'),Show.start_time).filter(Venue.id==Show.venue_id).filter(Show.artist_id==Artist.id).filter(Venue.id==venue_id).filter(Show.start_time >= datetime.datetime.now()).all()
 
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

  except:
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue "' + request.form['name'] + '" could not be listed.', 'alert-danger')
    db.session.rollback()
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.with_entities(Artist.id, Artist.name).all()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
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
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
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

    data = request.form
    new_artist = Artist()

    if data.get('name'):
      new_artist.name = data.get('name')

    if data.get('city'):
      new_artist.city = data.get('city')

    if data.get('state'):
      new_artist.state = data.get('state')

    if data.get('phone'):
      new_artist.phone = data.get('phone')

    if data.get('image_link'):
      new_artist.image_link = data.get('image_link')

    if data.get('facebook_link'):
      new_artist.facebook_link = data.get('facebook_link')

    if data.get('seeking_venue'):
      new_artist.seeking_venue = True

    if data.get('seeking_description'):
      new_artist.seeking_description = data.get('seeking_description')

    if data.getlist('genres'):
      for item in data.getlist('genres'):
        new_genre = Genre.query.filter(Genre.name==item).first()
        if new_genre:
          new_artist.genres.append(new_genre)

    if data.get('website_link'):
      new_artist.website = data.get('website_link')
  
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

    data = request.form

    new_show = Show()

    if data.get('artist_id'):
      new_show.artist_id = data.get('artist_id')

    if data.get('venue_id'):
      new_show.venue_id = data.get('venue_id')

    if data.get('start_time'):
      new_show.start_time = data.get('start_time')

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
