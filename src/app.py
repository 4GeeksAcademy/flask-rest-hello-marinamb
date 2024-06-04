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
from models import db, User, People, Planets, Favorite_people, Favorite_planet
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
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    serialized_people = [person.serialize() for person in people]
    return jsonify(serialized_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    people = People.query.get(people_id)
    if people : 
        serialized_people = people.serialize()
        return jsonify(serialized_people)
    else : 
        return jsonify({"msg" : "person not found"}), 400
    

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    serialized_planets = [planet.serialize() for planet in planets]
    return jsonify(serialized_planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planets = Planets.query.get(planet_id)
    if planets : 
        serialized_planets = planets.serialize()
        return jsonify(serialized_planets)
    else : 
        return jsonify({"msg" : "planet not found"}), 400
    

@app.route('/favorite/people_id', methods=['POST'])
def add_people_favorite():
    data = request.json
    user_id = data["user_id"]
    people_id = data['people_id']
    
    new_people_favorite = Favorite_people(
        user_id=user_id, people_id=people_id
    )
    db.session.add(new_people_favorite)
    db.session.commit()
    
    return jsonify(data), 200

@app.route('/favorite/planet_id', methods=['POST'])
def add_planet_favorite():
    data = request.json
    user_id = data["user_id"]
    planet_id = data['planet_id']
    
    new_planet_favorite = Favorite_planet(
        user_id=user_id, planet_id=planet_id
    )
    db.session.add(new_planet_favorite)
    db.session.commit()
    
    return jsonify(data), 200

@app.route('/favorite/<int:favorite_type_id>', methods=['DELETE'])
def remove_favorite(favorite_type_id):
    data = request.json
    user_id = data["user_id"]
    
    if favorite_type_id == 1:
        people_id = data["people_id"]
        remove_fav_people = Favorite_people.query.filter_by(user_id=user_id, people_id=people_id).first()
        if remove_fav_people:
            db.session.delete(remove_fav_people)
            db.session.commit()
            return jsonify({"msg": "Favortie people remove"}), 200
    elif favorite_type_id == 2:
        planet_id = data["planet_id"]
        remove_fav_planet = Favorite_planet.query.filter_by(user_id=user_id, planet_id=planet_id).first()   
        if remove_fav_planet:
            db.session.delete(remove_fav_planet)
            db.session.commit()
            return jsonify({"msg": "Favortie planet remove"}), 200
    return jsonify({"msg": "Favortie not found"}), 404
    
 
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
