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
from models import db, User, Characters, Planets, Favorites
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

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////   METODOS GET  //////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200

#----------GET DE TODOS LOS PERSONAJES
@app.route('/people', methods=['GET'])
def get_all_characters():
    character = Characters.query.all()

    serialize_char = [char.serialize() for char in character]
    return jsonify(serialize_char),200

#----------GET DE UN PERSONAJE
@app.route('/people/<int:id>', methods=['GET'])
def get_one_characters(id):
    character = Characters.query.get(id)

    if not character:
        return jsonify({"message": "not found"}), 404
    
    
    return jsonify(character.serialize()), 200


#----------GET DE TODOS LOS PLANETAS
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planet = Planets.query.all()

    serialize_planet = [pl.serialize() for pl in planet]

    return jsonify(serialize_planet),200


#----------GET DE UN PLANETA

@app.route('/planets/<int:id>',methods=['GET'])
def get_one_planet(id):
    planet = Planets.query.get(id)

    if planet:
        return jsonify({"message":"not found"}),404
    
    return jsonify(planet.serialize())

#----------GET DE LOS USUARIOS
@app.route('/users', methods=['GET'])
def get_users():
    user = User.query.all()

    serialize_user = [us.serialize() for us in user if us.is_active]

    return jsonify(serialize_user),201

#----------GET DE LOS FAVORITOS DE UN USUARIO
@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    favorite = Favorites.query.filter_by(user_id=1).all()
    if not favorite:
        return jsonify({"msg":"not exist"}),404
    
    favorite_serialized = [fav.serialize() for fav in favorite]
    return jsonify(favorite_serialized),200
    

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////   METODOS POST  /////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#----------METODO PARA AÑADIR UN PERSONAJE FAVORITO AL USUARIO 

@app.route('/favorite/people/<int:id>', methods=['POST'])
def add_favorite_character(id):
    favorite = Favorites(char_id = id,user_id = 1,planet_id = None)
    db.session.add(favorite)
    db.session.commit()

    # exist = Favorites.query.filter_by(char_id=id,user_id=1)

    # if exist:
    #     return ({"message":"already exist"}),409

    return jsonify(favorite.serialize()),200


#----------METODO PARA AÑADIR UN PLANETA FAVORITO AL USUARIO 

@app.route('/favorite/planet/<int:id>', methods=['POST'])
def add_favorite_planet(id):
    # exist = Favorites.query.filter_by(planet_id=id,user_id=1)

    # if exist:
    #     return ({"message":"Not found"}),409
    
    favorite = Favorites()
    favorite.char_id = None
    favorite.user_id = 1
    favorite.planet_id = id

    db.session.add(favorite)
    db.session.commit()

    return jsonify(favorite.serialize()),201
    
    

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////   METODOS DELETE  //////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#----------METODO DELETE PARA AÑADIR UN PERSONAJE FAVORITO AL USUARIO 

@app.route('/favorite/people/<int:id>', methods=['DELETE'])
def delete_favorite_char(id):
    exist= Favorites.query.filter_by(char_id=id,user_id=1).first()
    
    if not exist:
        return ({'message':'not exist'}),404
    
    db.session.delete(exist)
    db.session.commit()
    return jsonify(exist.serialize()),200

#----------METODO DELETE PARA AÑADIR UN PLANETA FAVORITO AL USUARIO 

@app.route('/favorite/planet/<int:id>', methods=['DELETE'])
def delete_favorite_planet(id):
    exist= Favorites.query.filter_by(planet_id=id,user_id=1).first()
    
    if not exist:
        return ({'message':'not exist'}),404
    
    db.session.delete(exist)
    db.session.commit()
    return jsonify(exist.serialize()),200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
