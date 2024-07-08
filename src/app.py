"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favourites, Characters, Planets, Vehicles

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    all_users = [user.serialize() for user in users]
    return jsonify(all_users), 200

@app.route('/people', methods=['GET'])
def get_all_characters():
    characters = Characters.query.all()
    all_characters = [character.serialize() for character in characters]
    return jsonify(all_characters), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):
    character = Characters.query.get(people_id)
    if not character:
        return jsonify({'error': 'Character not found'}), 404
    return jsonify(character.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planets.query.all()
    all_planets = [planet.serialize() for planet in planets]
    return jsonify(all_planets), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planet(planets_id):
    planet = Planets.query.get(planets_id)
    if not planet:
        return jsonify({'error': 'Planet not found'}), 404
    return jsonify(planet.serialize()), 200

@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    vehicles = Vehicles.query.all()
    all_vehicles = [vehicle.serialize() for vehicle in vehicles]
    return jsonify(all_vehicles), 200

@app.route('/vehicles/<int:vehicles_id>', methods=['GET'])
def get_vehicle(vehicles_id):
    vehicle = Vehicles.query.get(vehicles_id)
    if not vehicle:
        return jsonify({'error': 'Vehicle not found'}), 404
    return jsonify(vehicle.serialize()), 200

@app.route('/users/<int:user_id>/favourites', methods=['GET'])
def get_user_favourites(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    favourites = user.favourites
    all_favourites = [favourite.serialize() for favourite in favourites]
    return jsonify(all_favourites), 200

@app.route('/favourite/planet/<int:planets_id>', methods=['POST'])
def add_favourite_planet(planets_id):
    user_id = request.headers.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    planet = Planets.query.get(planets_id)
    if not planet:
        return jsonify({'error': 'Planet not found'}), 404

    favourite_planet = Favourites(user_id=user.id, planet_id=planet.id)
    db.session.add(favourite_planet)
    db.session.commit()

    return jsonify({'msg': 'Favourite planet added successfully'}), 200

@app.route('/favourite/characters/<int:characters_id>', methods=['POST'])
def add_favorite_character(characters_id):
    user_id = request.headers.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    character = Characters.query.get(characters_id)
    if not character:
        return jsonify({'error': 'Character not found'}), 404

    favourite_character = Favourites(user_id=user.id, character_id=character.id)
    db.session.add(favourite_character)
    db.session.commit()

    return jsonify({'msg': 'Favourite character added successfully'}), 200

@app.route('/favourite/planet/<int:planets_id>', methods=['DELETE'])
def delete_favourite_planet(planets_id):
    user_id = request.headers.get('user_id')
    favourite_planet = Favourites.query.filter_by(user_id=user_id, planet_id=planets_id).first()
    if not favourite_planet:
        return jsonify({'error': 'Favourite planet not found'}), 404

    db.session.delete(favourite_planet)
    db.session.commit()

    return jsonify({'msg': 'Favourite planet deleted successfully'}), 200

@app.route('/favourite/characters/<int:characters_id>', methods=['DELETE'])
def delete_favourite_character(characters_id):
    user_id = request.headers.get('user_id')
    favourite_character = Favourites.query.filter_by(user_id=user_id, character_id=characters_id).first()
    if not favourite_character:
        return jsonify({'error': 'Favourite character not found'}), 404

    db.session.delete(favourite_character)
    db.session.commit()

    return jsonify({'msg': 'Favourite character deleted successfully'}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)