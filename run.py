# Esto lo ponemos para cuando ejecutemos con uWSGI, para evitar imports circulares
# Ya que con uWSGI no se pasa for el if __name__="__main__"
from app import app
from db import db

db.init_app(app)

#ueremos que alchemy nos cree las tablas
@app.before_first_request
def create_tables():
    db.create_all()