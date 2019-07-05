from flask_restful import Resource, reqparse
from models.examen import ExamenModel
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity, get_raw_jwt
from datetime import datetime

class ExamenGenerico:
    parser = reqparse.RequestParser()
    parser.add_argument('id',
        type=int
    )
    parser.add_argument('fecha',
        type=str,
        required=True,
        help="date of the exam is mandatory"
    )
    parser.add_argument('aciertos',
        type=int,
        required=True,
        help="Number of correct answers is mandatory"
    )
    parser.add_argument('fallos',
        type=int,
        required=True,
        help="Number of wrong answers is mandatory"
    )
    

class Examen(Resource, ExamenGenerico):
    @jwt_required
    def get(self, id):
        examen = ExamenModel.find_by_exam_id_and_user_id(id, get_jwt_identity())
        if examen:
            return examen.json()
        return {'message': 'Examen not found'}, 404

    @fresh_jwt_required
    def put(self, id):
        print("hola", id)
        data = Examen.parser.parse_args()
        examen = ExamenModel.find_by_exam_id_and_user_id(id, get_jwt_identity())
        if examen is None:
            return {'message': 'Examen not found '}, 404
        else:
            examen.fecha = datetime.strptime(data['fecha'], '%d/%m/%Y %H:%M:%S')
            examen.aciertos = data['aciertos']
            examen.fallos = data['fallos']
            examen.save_to_db()
            return examen.json()

    @fresh_jwt_required
    def delete(self, id):
        examen = ExamenModel.find_by_exam_id_and_user_id(id, get_jwt_identity())     
        if examen:
            examen.delete_from_db()
            return {'message':'Exam deleted'}
        else:
            return {'message':'Something happened while deleting Exam. Maybe it doesnt exist or youre not allowed to do so'}

    
class ExamenNuevo(Resource, ExamenGenerico):
    @fresh_jwt_required
    def post(self):      
        data = Examen.parser.parse_args()
        fecha = datetime.strptime(data['fecha'], '%d/%m/%Y %H:%M:%S')
        term = ExamenModel(
                        fecha, 
                        data['aciertos'], 
                        data['fallos'],
                        get_jwt_identity()
        )
        try:
            term.save_to_db()
        except:
            return {"message": "An error occurred inserting term. "}, 500
        return term.json(), 201  
    

class ExamenesList(Resource):
    @jwt_required
    def get(self):
        terminos = ExamenModel.find_by_user_id(get_jwt_identity())
        return {'examenes': [termino.json() for termino in terminos.all()]}