from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import User, UserRegister, UserLogin, TokenRefresh, TokenExpire
from resources.termino import TerminoNuevo, TerminosList, Termino
from resources.examen import ExamenNuevo, ExamenesList, Examen
from resources.items import Item, ItemNuevo, ItemsList 
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://uservocabulariodb:uservocabulariodb@localhost/vocabulariodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

@app.before_first_request
def create_tables():
    db.create_all()
app.secret_key = 's3cr3ti110_12345*'

api = Api(app)
jwt = JWTManager(app)



@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return TokenExpire.is_token_expired(jti)


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify(
        {
            "description": "Token has expired!",
            "error": "token_expired"
    }), 401
    

@jwt.invalid_token_loader
def invalid_token_callback():
    return jsonify(
        {
            "description": "Signature verification failed!",
            "error": "invalid_token"
    }), 401
    


@jwt.unauthorized_loader
def unauthorized_loader_callback(error):
    return jsonify(
        {
            "description": "Access token not found!",
            "error": "unauthorized_loader"
    }), 401

# Authentication endpoints
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserRegister, "/auth/register")
api.add_resource(UserLogin, "/auth/login")
api.add_resource(TokenRefresh, "/auth/refresh")
api.add_resource(TokenExpire, "/auth/logout")

# Terms endpoints
api.add_resource(TerminosList, "/terms")
api.add_resource(Termino, "/term/<int:id>")
api.add_resource(TerminoNuevo, "/term")

# Exams endpoints
api.add_resource(ExamenesList, "/exams")
api.add_resource(Examen, "/exam/<int:id>")
api.add_resource(ExamenNuevo, "/exam")

# Exam items endpoints
api.add_resource(ItemsList, "/exam/<int:examen_id>/items")
api.add_resource(Item, "/exam/<int:examen_id>/<int:termino_id>")
api.add_resource(ItemNuevo, "/item")

# Con uWSGI no pasas por aquí, así que no importas db
if __name__ == '__main__':
    # Imports circulares, si importamos db al princpio, y en models también vas a crear una importación circular
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)