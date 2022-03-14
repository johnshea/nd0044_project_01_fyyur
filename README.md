# Fyyur

This is the first project in Udacity's Full Stack Web Developer Nanodegree Program.

This project was to build out the data models to power the API endpoints for the Fyyur site by connecting to a PostgreSQL database for storing, querying, and creating information about artists and venues on Fyyur.

This project requires a working PostgreSQL server.

## Project Setup
Clone the project repository.
```bash
git clone https://github.com/johnshea/nd0044_project_01_fyyur.git
```
Create a virtual environment.
```bash
python3 -m venv env
```
Activate the virtual environment.
```bash
source ./env/bin/activate
```
Install the required project dependencies.
```bash
pip3 install -r requirements.txt
```

Create the Postgres Database.
```bash
createdb fyyur
```
Define the flask environment variables.
```
export FLASK_APP=app.py
export FLASK_DEBUG=true
```
Setup the database schema by running the migration scripts.
```
flask db upgrade
```
There are two database seeding options.
- Option A - Bare minimum. Only table `genres` is populated. No data is populated for Artists, Venues, nor Shows. App fully functions but the user must create all Artist, Venue, and Show data.
- Option B - Database is fully populated with data for Artists, Venues, Shows, and Genres.

Steps for Option A

Log into the database and populate table `genres`.
NOTE - This table needs to be populated for the app to work.
```
psql fyyur

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
```

Steps for Option B

Log into the database and run all db lines from file `project_01_fyyur_db_seed.sql`.
NOTE - Data for table `genres` is contained in this file. You should not load table `genres` as described in "Steps for Option A".

NOTE - The database configuration setting are stored in file `config.py` in constant `SQLALCHEMY_DATABASE_URI`.

Run the app.
```
flask run
```

Open a browser and navigate to http://127.0.0.1:5000/
#
_NOTE_: When finished, to exit the virtual environment run:
```bash
deactivate
```
