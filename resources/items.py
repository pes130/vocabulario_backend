from flask_restful import Resource, reqparse
from models.items import ItemModel
from models.examen import ExamenModel
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity


class ItemGenerico():
    parser = reqparse.RequestParser()
    parser.add_argument('termino_id',
        type=int,
        required=True,
        help="Field 'termino_id' is mandatory"
    )
    parser.add_argument('examen_id',
        type=int,
        required=True,
        help="Field 'examen_id' is mandatory"
    )
    parser.add_argument('acierto',
        type=bool
    )

class Item(Resource, ItemGenerico):
    
    @jwt_required
    def get(self, termino_id, examen_id):
        item = ItemModel.find_by_id_termino_examen(termino_id, examen_id)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @fresh_jwt_required
    def delete(self, termino_id, examen_id):
        item = ItemModel.find_by_id_termino_examen(termino_id, examen_id)
        if item:
            item.delete_from_db()
        return {'message':'Exam item deleted'}

    @fresh_jwt_required
    def put(self, termino_id, examen_id):
        data = ItemGenerico.parser.parse_args()
        item = ItemModel.find_by_id_termino_examen(termino_id, examen_id)
        if item is None:
            return {'message': 'Exam item not found '}, 404
        else:
            item.acierto = data['acierto'] 
            item.save_to_db()
            return item.json()


class ItemNuevo(Resource, ItemGenerico):
    @fresh_jwt_required
    def post(self):
        data = ItemGenerico.parser.parse_args()
        examen = ExamenModel.find_by_exam_id_and_user_id(data['examen_id'], get_jwt_identity())
        if examen is None:
            return {'message': "No exam with id {} found".format(data['examen_id'])}, 400 #Bad request    
        item = ItemModel.find_by_id_termino_examen(data['termino_id'], data['examen_id'])
        if item is not None:
            return {'message': "This term is already in this exam"}, 400 #Bad request    
        item = ItemModel (
                        data['termino_id'],
                        data['examen_id'],
                        data['acierto']
        )
        try:
            item.save_to_db()
        except:
            return {"message": "An error occured creating item for exam"}, 500
        return item.json(), 201      


class ItemsList(Resource):
    @jwt_required
    def get(self, examen_id):
        #current_user_id = get_jwt_identity()
        items = ItemModel.find_by_examen_id(examen_id)
        return {'preguntas': [item.json() for item in items.all()]}




    
