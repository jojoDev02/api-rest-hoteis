from flask_restful import Resource, reqparse
from blacklist import BLACKLIST
from models.user import UserModel
import hmac
from flask_jwt_extended import create_access_token, get_jwt, jwt_required


argumentos = reqparse.RequestParser()
argumentos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank.")   
argumentos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank.")

class User(Resource):
    # /user/{user_id}
   
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user: 
            return user.json()
        return {'message': 'User not found.'}, 404
    
    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)

        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An internal error ocurred trying to delete user.'},500
            return {'message' : 'user deleted'}
        return {'message' : 'user not found'}, 404

class UserRegister(Resource):
    # /cadastro
   def post(self):
   

    dados = argumentos.parse_args()

    if UserModel.find_by_login(dados['login']):
        return {"message": "The login '{}' already exists.".format(dados['login'])}, 400
    
    user = UserModel(**dados)

    try:
        user.save_user()
    except:
        return {'message' : 'An internal error ocurred trying to save user.'}, 500
    return{'message':'User cread successfuly!'}, 201 #CREATED
   
class UserLogin(Resource):
    # /login
    @classmethod
    def post(cls):
        dados = argumentos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and hmac.compare_digest(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity = user.user_id)
            return {'access_token' : token_de_acesso}
        return{'message' : 'The username or password is incorrect.'}, 401 

class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return{'message' : 'Logged out successfully!'}, 200

