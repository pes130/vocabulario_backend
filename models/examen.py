from db import db
from datetime import datetime

class ExamenModel(db.Model):
    __tablename__ = 'examenes'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime)
    aciertos = db.Column(db.Integer)
    fallos = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    preguntas = db.relationship('ItemModel', lazy='dynamic') 

    def __init__(self, fecha, aciertos, fallos, user_id):
        self.fecha = fecha
        self.aciertos = aciertos
        self.fallos = fallos
        self.user_id = user_id
    
    def json(self):
        return {
            'id': self.id,
            'fecha': self.fecha.strftime('%d/%m/%Y %H:%M:%S'), 
            'aciertos': self.aciertos,
            'fallos': self.fallos,
            'preguntas': [item.json2() for item in self.preguntas.all()]
        }

    @classmethod
    def find_by_user_id(cls, user_id):
        return ExamenModel.query.filter_by(user_id=user_id).order_by(ExamenModel.fecha.desc())
    
    @classmethod
    def find_by_exam_id_and_user_id(cls, exam_id, user_id):
        return ExamenModel.query.filter_by(id=exam_id).filter_by(user_id=user_id).first()
    
    @classmethod
    def find_by_id(cls, id):
        return ExamenModel.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()