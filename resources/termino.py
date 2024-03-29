from flask_restful import Resource, reqparse
from models.termino import TerminoModel
from models.examen import ExamenModel
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity, get_raw_jwt
from resources.models.resultado import TerminoResultado

class TerminoGenerico:
    parser = reqparse.RequestParser()
    parser.add_argument('id',
        type=int
    )
    parser.add_argument('termino',
        type=str,
        required=True,
        help="'Termino' field is mandatory"
    )
    parser.add_argument('definicion',
        type=str,
        required=True,
        help="'Termino' field is mandatory"
    )
    parser.add_argument('ejemplo',
        type=str
    )
    parser.add_argument('tipo',
        type=str
    )
    parser.add_argument('user_id',
        type=str
    )

class Termino(Resource, TerminoGenerico):
    @jwt_required
    def get(self, id):
        termino = TerminoModel.find_by_termino_and_user_id(id, get_jwt_identity())
        if termino:
            return termino.json()
        return {'message': 'Term not found'}, 404

    @fresh_jwt_required
    def put(self, id):
        print("hola", id)
        data = Termino.parser.parse_args()
        term = TerminoModel.find_by_id(id)
        if term is None:
            return {'message': 'Term not found '}, 404
        else:
            # El id no se debería cambiar
            # term.id = id
            term.termino = data['termino']
            term.definicion = data['definicion']
            term.ejemplo = data['ejemplo']
            term.tipo = data['tipo']
            # El usuario_id no se debería cambiar!!!
            term.save_to_db()
            return term.json()

    @fresh_jwt_required
    def delete(self, id):
        term = TerminoModel.find_by_id(id)
        current_user_id = get_jwt_identity()
        if term and term.user_id == current_user_id:
            term.delete_from_db()
            return {'message':'Term deleted'}
        else:
            return {'message':'Something happened while deleting term. Maybe it doesnt exist or youre not allowed to do so'}

    
class TerminoNuevo(Resource, TerminoGenerico):
    # termino, definicion, ejemplo, tipo, user_id):
    @fresh_jwt_required
    def post(self):      
        data = Termino.parser.parse_args()
        # Recuperamos el usuario actual. Recuerda que lo seteamos en el login
        current_user_id = get_jwt_identity()
        term = TerminoModel.find_by_termino_and_user_id(data['termino'], current_user_id)
        if term is not None:
            return {'message': "Term '{}' already exists!.".format(data['termino'])}, 400 #Bad request    
        
       
        term = TerminoModel(
                        data['termino'], 
                        data['definicion'], 
                        data['ejemplo'], 
                        data['tipo'],
                        current_user_id
        )
        try:
            term.save_to_db()
        except:
            return {"message": "An error occurred inserting term. "}, 500
        return term.json(), 201  
    

class TerminosList(Resource):
    @jwt_required
    def get(self):
        current_user_id = get_jwt_identity()
        terminos = TerminoModel.find_by_user_id(current_user_id)
        return {'terminos': [termino.json() for termino in terminos.all()]}

class TerminosPorTipoList(Resource):
    @jwt_required
    def get(self, tipo):
        current_user_id = get_jwt_identity()
        terminos = TerminoModel.find_by_tipo_and_user_id(tipo, current_user_id)
        return {'terminos': [termino.json() for termino in terminos.all()]}

class TiposDeTerminos(Resource):
    @jwt_required
    def get(self):
        current_user_id = get_jwt_identity()
        tipos = TerminoModel.find_tipos_by_user_id(current_user_id)
        return {'tipos': [tipo[0] for tipo in tipos.all()]}
    

class TerminosResultados(Resource):
    @jwt_required
    def get(self):
        current_user_id = get_jwt_identity()
        examenes = ExamenModel.find_by_user_id(get_jwt_identity())
        terminos = TerminoModel.find_by_user_id(current_user_id)

        resultados = {}
        terminos_dict = {termino.id: termino for termino in terminos.all()}
        
        for examen in examenes.all():
            for pregunta in examen.preguntas:
                if resultados.get(pregunta.termino_id) is None:
                    if pregunta.acierto:
                        resultados[pregunta.termino_id] = TerminoResultado(terminos_dict[pregunta.termino_id].termino, 1, 0)
                    else:
                        resultados[pregunta.termino_id] = TerminoResultado(terminos_dict[pregunta.termino_id].termino, 0, 1)
                else:
                    if pregunta.acierto:
                        resultados[pregunta.termino_id].aciertos+=1
                    else:
                        resultados[pregunta.termino_id].fallos+=1 
        return {'resultados': [resultado.json() for resultado in resultados.values()]}