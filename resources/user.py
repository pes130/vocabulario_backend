from flask_restful import Resource, reqparse
from models.user import UserModel
from models.blacklist import BlacklistModel
from flask_jwt_extended import decode_token, create_access_token, get_csrf_token, get_jti, create_refresh_token, jwt_refresh_token_required, jwt_required, get_jwt_identity, get_raw_jwt

import hashlib

_usuario_parser = reqparse.RequestParser()
_usuario_parser.add_argument(
    "username",
    type=str,
    required=True,
    help="username field could not be empty"
)
_usuario_parser.add_argument(
    "password",
    type=str,
    required=True,
    help="password field could not be empty"
)

class User(Resource):
    def get(self, _id):
        user = UserModel.find_by_id(_id)
        if user:
            return user.json()
        else:
            return {
                "message": "User not found!"
            }, 404

class UserRegister(Resource):
    def post(self):
        data = _usuario_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {
                "message": "User exists!!"
            }, 400
        user = UserModel(data['username'], hashlib.sha256(data["password"].encode("utf-8")).hexdigest())
        user.save_to_db()
        return {"message": "User {} created!".format(data["username"])}

class UserLogin(Resource):
    def post(self):
        data = _usuario_parser.parse_args()

        user = UserModel.find_by_username(data['username'])
        if user and user.password == hashlib.sha256(data["password"].encode("utf-8")).hexdigest():
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            token_info = decode_token(access_token)
            expires = token_info['exp']
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires": expires
            }, 200
        return {
            "message": "Invalid credentials!"
        }, 401

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user_id = get_jwt_identity()
        new_token = create_access_token(identity=current_user_id, fresh=False)
        token_info = decode_token(new_token)
        expires = token_info['exp']
        return {
            "access_token": new_token,
            "expires": expires
        }, 200

class TokenExpire(Resource):

    @jwt_required
    def delete(self):
        raw_jwt = get_raw_jwt()
        jti = raw_jwt['jti']
        print("----------------------------------"+jti)
        token2Add = BlacklistModel(jti)
        token2Add.save_to_db()
        return {
            "message": "Succesfully logged out",
        }, 200

    @classmethod
    def is_token_expired(cls, token):
        return BlacklistModel.find_by_token(token)