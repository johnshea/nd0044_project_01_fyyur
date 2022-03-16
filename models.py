from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
    shows = db.relationship("Show", backref="venue", cascade="all, delete")

    def __repr__(self):
      return f'<Venue id={self.id}, name=\'{self.name}\'>'


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
    shows = db.relationship("Show", backref="artist", cascade="all, delete")

    def __repr__(self):
      return f'<Artist id={self.id}, name=\'{self.name}\'>'


class Genre(db.Model):
    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)

    def __repr__(self):
      return f'<Genre id={self.id}, name=\'{self.name}\'>'
