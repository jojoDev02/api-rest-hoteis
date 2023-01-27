from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from resources.filters import consulta_com_cidade, consulta_sem_cidade, normalize_path_params
from flask_jwt_extended import jwt_required
import sqlite3



# path /hoteis?cidade = Rio de Janeiro&estrelas_min = 4&diaria_max = 400
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str, location= 'values')
path_params.add_argument('estrelas_min', type=float , location= 'values')
path_params.add_argument('estrelas_max', type=float, location= 'values')
path_params.add_argument('diaria_min', type = float, location= 'values')
path_params.add_argument('diaria_max', type=float, location= 'values')
path_params.add_argument('limit', type= int, location= 'values')
path_params.add_argument('offset', type= int, location= 'values')

    
class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('instance/banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {chave : dados[chave] for chave in dados if dados[chave] is not None}
        params = normalize_path_params(**dados_validos)

        print(params)

        if params.get('cidade'):
            tupla = tuple([params[chave] for chave in params])
            resultado = cursor.execute(consulta_com_cidade, tupla) 
        else:
            tupla = tuple([params[chave] for chave in params])
            resultado = cursor.execute(consulta_sem_cidade, tupla)
          
        
        hoteis=[]
        for linha in resultado:
            hoteis.append({
                'hotel_id' : linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'valor_diaria': linha[3],
                'cidade' :linha[4]
        })

        connection.close()
        return {'hoteis': hoteis} 

class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank.")   
    argumentos.add_argument('estrelas', type=float)
    argumentos.add_argument('valor_diaria', type=float)
    argumentos.add_argument('cidade', type=str, required=True, help="The field 'cidade' cannot be left blank.")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404
    
    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return{'message' : "Hotel id {} already exists.".format(hotel_id)}, 400
        
        dados = Hotel.argumentos.parse_args()  
        hotel= HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 # internal server error 
        return hotel.json(), 201 

    @jwt_required()
    def put(self, hotel_id):

        dados = Hotel.argumentos.parse_args()

        hotel_found = HotelModel.find_hotel(hotel_id)

        if hotel_found:
            hotel_found.update_hotel(**dados)
            hotel_found.save_hotel()
            return hotel_found.json(), 200 #update
        
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500
        return hotel.json(), 201 #created

    @jwt_required() 
    def delete(self, hotel_id):

        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal error ocurred trying to delete hotel.'},500
            return {'message' : 'hotel deleted'}
        return {'message' : 'hotel not found'}, 404