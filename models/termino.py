from db import db

class TerminoModel(db.Model):
    __tablename__ = 'terminos'
    id = db.Column(db.Integer, primary_key=True)
    termino = db.Column(db.String(100))
    definicion = db.Column(db.Text)
    ejemplo = db.Column(db.Text)
    tipo = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))


    def __init__(self, termino, definicion, ejemplo, tipo, user_id):
        self.termino = termino
        self.definicion = definicion
        self.ejemplo = ejemplo
        self.tipo = tipo
        self.user_id = user_id
    
    def json(self):
        # devuelves un diccionario
        return {
            'id': self.id,
            'termino': self.termino, 
            'definicion': self.definicion,
            'ejemplo': self.ejemplo,
            'tipo': self.tipo
        }

    @classmethod
    def find_by_user_id(cls, user_id):
        return TerminoModel.query.filter_by(user_id=user_id)
    
    @classmethod
    def find_by_id(cls, id):
        return TerminoModel.query.filter_by(id=id).first()

    @classmethod
    def find_by_termino(cls, termino):
        return TerminoModel.query.filter_by(termino=termino).first()

    @classmethod
    def find_by_termino_and_user_id(cls, termino, user_id):
        return TerminoModel.query.filter_by(termino=termino).filter_by(user_id=user_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()