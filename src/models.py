from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favourites = db.relationship("Favourites", uselist=False, lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Favourites(db.Model):
    __tablename__ = 'favourites'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id),nullable=False)
    user = db.relationship("User", back_populates="favourites")
    characters = db.relationship("Characters", lazy=True)
    planets = db.relationship("Planets", lazy=True)
    vehicles = db.relationship("Vehicles", lazy=True)
    
    def serialize(self):
        return {
            "id": self.id,
        }
    
class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    birth_year = db.Column(db.String(20), unique=False, nullable=False)
    gender = db.Column(db.String(20), unique=False, nullable=False)
    homeworld = db.Column(db.String(20), unique=False, nullable=False)
    species = db.Column(db.String(200), unique=False, nullable=False)
    favourite_id = db.Column(db.Integer, db.ForeignKey('favourites.id'),nullable=True)
    favourite = db.relationship('Favourites', back_populates = 'characters')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld,
            "species": self.species,
            "favourite_id": self.favourite_id,              
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    climate = db.Column(db.String(20), unique=False, nullable=False)
    terrain = db.Column(db.String(20), unique=False, nullable=False)
    favourite_id = db.Column(db.Integer, db.ForeignKey('favourites.id'),nullable=True)
    favourite = db.relationship('Favourites', back_populates = 'planets')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "favourite_id": self.favourite_id,              
        }
    
class Vehicles (db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    model = db.Column(db.String(20), unique=False, nullable=False)
    manufacturer = db.Column(db.String(20), unique=False, nullable=False)
    favourite_id = db.Column(db.Integer, db.ForeignKey('favourites.id'),nullable=True)
    favourite = db.relationship('Favourites', back_populates = 'vehicles')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "favourite_id": self.favourite_id,              
        }