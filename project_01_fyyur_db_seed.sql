INSERT INTO venues (
  name
  ,address
  ,city
  ,state
  ,phone
  ,image_link
  ,facebook_link
  ,seeking_talent
  ,seeking_description
  ,website
)
VALUES (
  'The Musical Hop'
  ,'1015 Folsom Street'
  ,'San Francisco'
  ,'CA'
  ,'123-123-1234'
  ,'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60'
  ,'https://www.facebook.com/TheMusicalHop'
  ,true
  ,'We are on the lookout for a local artist to play every two weeks. Please call us.'
  ,'https://www.themusicalhop.com'
);

INSERT INTO venues (
  name
  ,address
  ,city
  ,state
  ,phone
  ,image_link
  ,facebook_link
  ,seeking_talent
  ,website)
VALUES (
  'The Dueling Pianos Bar'
  ,'335 Delancey Street'
  ,'New York'
  ,'NY'
  ,'914-003-1132'
  ,'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80'
  ,'https://www.facebook.com/theduelingpianos'
  ,false
  ,'https://www.theduelingpianos.com'
);

INSERT INTO venues (
  name
  ,address
  ,city
  ,state
  ,phone
  ,image_link
  ,facebook_link
  ,seeking_talent
  ,website
) VALUES (
  'Park Square Live Music & Coffee'
  ,'34 Whiskey Moore Ave'
  ,'San Francisco'
  ,'CA'
  ,'415-000-1234'
  ,'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80'
  ,'https://www.facebook.com/ParkSquareLiveMusicAndCoffee'
  ,false
  ,'https://www.parksquarelivemusicandcoffee.com'
);



-- 1
INSERT INTO artists (name) VALUES ('Artist One');
-- 2
INSERT INTO artists (name) VALUES ('Artist Two');
-- 3
INSERT INTO artists (name) VALUES ('Artist Three');
-- 4
INSERT INTO artists (
  name
  ,city
  ,state
  ,phone
  ,website
  ,image_link
  ,facebook_link
  ,seeking_venue
  ,seeking_description
) VALUES (
  'Guns N Petals'
  ,'San Francisco'
  ,'CA'
  ,'326-123-5000'
  ,'https://www.gunsnpetalsband.com'
  ,'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80'
  ,'https://www.facebook.com/GunsNPetals'
  ,true
  ,'Looking for shows to perform at in the San Francisco Bay Area!'
);

-- 5
INSERT INTO artists (
  name
  ,image_link
  ,city
  ,state
  ,phone
  ,facebook_link
  ,seeking_venue
) VALUES (
  'Matt Quevedo'
  ,'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80'
  ,'New York'
  ,'NY'
  ,'300-400-5000'
  ,'https://www.facebook.com/mattquevedo923251523'
  ,false
);

-- 6
INSERT INTO artists (
  name
  ,image_link
  ,city
  ,state
  ,phone
  ,seeking_venue
) VALUES (
  'The Wild Sax Band'
  ,'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80'
  ,'San Francisco'
  ,'CA'
  ,'432-325-5432'
  ,false
);

DELETE FROM artists WHERE id < 4;

INSERT INTO genres (name) VALUES ('Jazz');
INSERT INTO genres (name) VALUES ('Reggae');
INSERT INTO genres (name) VALUES ('Swing');
INSERT INTO genres (name) VALUES ('Classical');
INSERT INTO genres (name) VALUES ('Folk');
INSERT INTO genres (name) VALUES ('R&B');
INSERT INTO genres (name) VALUES ('Hip-Hop');
INSERT INTO genres (name) VALUES ('Rock n Roll');


INSERT INTO genres (name) VALUES ('Alternative');
INSERT INTO genres (name) VALUES ('Blues');
INSERT INTO genres (name) VALUES ('Country');
INSERT INTO genres (name) VALUES ('Electronic');
INSERT INTO genres (name) VALUES ('Funk');
INSERT INTO genres (name) VALUES ('Heavy Metal');
INSERT INTO genres (name) VALUES ('Instrumental');
INSERT INTO genres (name) VALUES ('Musical Theatre');
INSERT INTO genres (name) VALUES ('Pop');
INSERT INTO genres (name) VALUES ('Punk');
INSERT INTO genres (name) VALUES ('Soul');
INSERT INTO genres (name) VALUES ('Other');

INSERT INTO artist_genre_association (artist_id, genre_id) VALUES (4, 8);
INSERT INTO artist_genre_association (artist_id, genre_id) VALUES (5, 1);
INSERT INTO artist_genre_association (artist_id, genre_id) VALUES (6, 1);
INSERT INTO artist_genre_association (artist_id, genre_id) VALUES (6, 4);

INSERT INTO venue_genre_association (venue_id, genre_id) VALUES (1, 1);
INSERT INTO venue_genre_association (venue_id, genre_id) VALUES (1, 2);
INSERT INTO venue_genre_association (venue_id, genre_id) VALUES (1, 3);
INSERT INTO venue_genre_association (venue_id, genre_id) VALUES (1, 4);
INSERT INTO venue_genre_association (venue_id, genre_id) VALUES (1, 5);

INSERT INTO venue_genre_association (venue_id, genre_id) VALUES (2, 4);
INSERT INTO venue_genre_association (venue_id, genre_id) VALUES (2, 6);
INSERT INTO venue_genre_association (venue_id, genre_id) VALUES (2, 7);

INSERT INTO venue_genre_association (venue_id, genre_id) VALUES (3, 8);
INSERT INTO venue_genre_association (venue_id, genre_id) VALUES (3, 1);
INSERT INTO venue_genre_association (venue_id, genre_id) VALUES (3, 4);
INSERT INTO venue_genre_association (venue_id, genre_id) VALUES (3, 5);

INSERT INTO shows (venue_id, artist_id, start_time) VALUES (1, 4, '2019-05-21T21:30:00.000Z');
INSERT INTO shows (venue_id, artist_id, start_time) VALUES (3, 5, '2019-06-15T23:00:00.000Z');
INSERT INTO shows (venue_id, artist_id, start_time) VALUES (3, 6, '2035-04-01T20:00:00.000Z');
INSERT INTO shows (venue_id, artist_id, start_time) VALUES (3, 6, '2035-04-08T20:00:00.000Z');
INSERT INTO shows (venue_id, artist_id, start_time) VALUES (3, 6, '2035-04-15T20:00:00.000Z');

