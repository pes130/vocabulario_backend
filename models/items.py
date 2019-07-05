from db import db
from datetime import datetime

class ItemModel(db.Model):
    __tablename__ = 'item_examenes'
    termino_id = db.Column(db.Integer, db.ForeignKey('terminos.id'), primary_key=True)
    examen_id = db.Column(db.Integer, db.ForeignKey('examenes.id'), primary_key=True)
    acierto = db.Column(db.Boolean)
    #pregunta = db.relationship('TerminoModel')
    pregunta = db.relationship('TerminoModel', cascade="all, delete-orphan",single_parent=True)
    
    def __init__(self, termino_id, examen_id, acierto):
        self.termino_id = termino_id
        self.examen_id = examen_id
        self.acierto = acierto
    
    def json(self):
        # devuelves un diccionario
        return {
            'termino_id': self.termino_id,
            'examen_id': self.examen_id, 
            'acierto': self.acierto
        }
    
    def json2(self):
        # devuelves un diccionario
        return {
            'termino': self.pregunta.json(),
            'acierto': self.acierto
        }

    @classmethod
    def find_by_examen_id(cls, examen_id):
        return ItemModel.query.filter_by(examen_id=examen_id)

    @classmethod
    def find_by_id_termino_examen(cls, termino_id, examen_id):
        return ItemModel.query.filter_by(examen_id=examen_id).filter_by(termino_id=termino_id).first()
  
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()