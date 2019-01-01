from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, jwt_optional
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

class User():
    def __init__(self, username='', password=''):
        self.username = username
        self.password = generate_password_hash(password)

@auth_blueprint.route('/login', methods=['GET'])
@jwt_optional
def login():
    user1 = User('Admin', '123')
    user2 = User('Guest', '456')
    users = (user1, user2)
    
    current_user = get_jwt_identity() 
    
    if current_user:
        return jsonify({"msg": "User already logged in as {}".format(current_user)}), 401    

    if not request.is_json:
        return jsonify({"msg": "Username and password required"}), 400    
    
    username = request.get_json().get("username", None)
    password = request.get_json().get("password", None)

    if not (username and password):
        return jsonify({"msg": "Username and password required"}), 400

    user_temp = None
    for user in users:
        if user.username == username:
            user_temp = user

    if user_temp and check_password_hash(user_temp.password, password):
        access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(minutes=15) 
)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Not authorized"}), 401 


@auth_blueprint.route('/jwt_test', methods=['GET'])
@jwt_required
def jwt_test():
    current_user = get_jwt_identity()
    if current_user:
        return jsonify({"msg": "User already logged in as {}".format(current_user)}), 401    
    else:
        return jsonify({"msg": "No user)"}), 200  