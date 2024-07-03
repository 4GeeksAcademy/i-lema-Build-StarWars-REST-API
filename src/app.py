"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favourites, Characters, Planets, Vehicles
#from models import Person

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
    all_users = list(map(lambda x: x.serialize(), users))

    return jsonify(all_users), 200



@app.route('/people', methods=['GET'])
def get_all_characters():

    characters = Characters.query.all()
    all_characters = list(map(lambda x: x.serialize(), characters))

    return jsonify(all_characters), 200



@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):

    character = Characters.query.get(people_id)
    one_character = character.serialize()

    return jsonify(one_character), 200



@app.route('/planets', methods=['GET'])
def get_all_planets():

    planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets))

    return jsonify(all_planets), 200



@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planet(planets_id):

    planet = Planets.query.get(planets_id)
    one_planet = planet.serialize()

    return jsonify(one_planet), 200



@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():

    vehicles = Vehicles.query.all()
    all_vehicles = list(map(lambda x: x.serialize(), vehicles))

    return jsonify(all_vehicles), 200


@app.route('/vehicles/<int:vehicles_id>', methods=['GET'])
def get_vehicle(vehicles_id):

    vehicle = Vehicles.query.get(vehicles_id)
    one_vehicle = vehicle.serialize()

    return jsonify(one_vehicle), 200



@app.route('/<int:user_id>/favourites', methods=['GET'])
def get_user_favourites(user_id):

    user = User.query.get(user_id)
    favourites = user.favourites  

    all_favourites = list(map(lambda x: x.serialize(), favourites))

    return jsonify(all_favourites), 200



@app.route('/favourite/planet/<int:planets_id>', methods=['POST'])
def add_favorite_planet(planets_id):

    user_id = request.headers.get('user_id')
    user = User.query.get(user_id)

    planet = Planets.query.get(planets_id)

    favourite_planet = Favourites(user_id=user.id, planet_id=planet.id)

    user.favourites.append(favourite_planet)

    db.session.commit()

    return jsonify({'message': 'Favorite planet added successfully'}), 200



@app.route('/favourite/characters/<int:characters_id>', methods=['POST'])
def add_favorite_character(characters_id):

    user_id = request.headers.get('user_id')
    user = User.query.get(user_id)

    character = Characters.query.get(characters_id)

    favourite_character= Favourites(user_id=user.id, character_id=character.id)

    user.favourites.append(favourite_character)

    db.session.commit()

    return jsonify({'message': 'Favorite character added successfully'}), 200



@app.route('/favorite/planet/<int:planets_id>', methods=['DELETE'])
def delete_favorite_planet(planets_id):
    
    favorite_planet = Favourites.query.filter_by(planet_id=planets_id).first()

    db.session.delete(favorite_planet)
    db.session.commit()
    return jsonify({'message': 'Favorite planet deleted successfully'}), 200


@app.route('/favorite/characters/<int:characters_id>', methods=['DELETE'])
def delete_favorite_character(characters_id):
    
    favorite_character = Favourites.query.filter_by(character_id=characters_id).first()

    db.session.delete(favorite_character)
    db.session.commit()
    return jsonify({'message': 'Favorite character deleted successfully'}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
