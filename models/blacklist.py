from db import db

class BlacklistModel(db.Model):
    __tablename__ = 'blacklist_tokens'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Text)

    def __init__(self, token):
        self.token = token
    
    def json(self):
        # devuelves un diccionario
        return {
            'id': self.id,
            'token': self.token
        }

    @classmethod
    def find_by_token(cls, token):
        return BlacklistModel.query.filter_by(token=token).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()