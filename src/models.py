from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)
    favourites = db.relationship("Favourites", backref="user", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Favourites(db.Model):
    __tablename__ = 'favourites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))

    character = db.relationship("Characters", backref="favourites")
    planet = db.relationship("Planets", backref="favourites")
    vehicle = db.relationship("Vehicles", backref="favourites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    birth_year = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    homeworld = db.Column(db.String(20), nullable=False)
    species = db.Column(db.String(200), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld,
            "species": self.species,
            "favourites": [fav.serialize() for fav in self.favourites]
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    climate = db.Column(db.String(20), nullable=False)
    terrain = db.Column(db.String(20), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "favourites": [fav.serialize() for fav in self.favourites]
        }

class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(20), nullable=False)
    manufacturer = db.Column(db.String(20), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "favourites": [fav.serialize() for fav in self.favourites]
        }