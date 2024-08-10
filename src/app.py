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
from models import (
    db,
    User,
    People,
    Planets,
    Favorites)
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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
def get_all():

    response = People.query.all()

    return jsonify(response), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def only_one():

    person = People.query.filter_by().people_id.first()

    return jsonify(person), 200


@app.route('/planets', methods=['GET'])
def all_planets():

    response = Planets.query.all()

    return jsonify(response), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def single_planet():

    world = Planets.query.filter_by().planet_id.first()

    return jsonify(world), 200


@app.route('/users', methods=['GET'])
def all_users():

    records = User.query.all()

    return jsonify(records), 200


@app.route('/users/favorites', methods=['GET'])
def favorited():

    liked = Favorites.filter_by('user_id').first()

    return jsonify(liked), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def favorite_planet():

    db.session.add('planet_id')
    db.commit('favorite')

    return 'success', 200


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def favorite_person():

    db.session.add('people_id')
    db.commit('favorite')

    return 'success', 200


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_planet():
    db.session.delete('planet_id')
    db.commit('favorite')

    return 'success', 200


@app.route('/favorite/planet/<int:people_id>', methods=['DELETE'])
def remove_person():
    db.session.delete('people_id')
    db.commit('favorite')

    return 'success', 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
