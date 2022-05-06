from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db=SQLAlchemy()
DB_Name='Database.db'

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='My Secret'
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_Name}'
    db.init_app(app)

    from .view import view
    from .auth import auth

    from .models import Student,Teacher
    create_database(app)
    
    app.register_blueprint(view,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    return app


def create_database(app):
    if not path.exists('website/'+DB_Name):
        db.create_all(app=app)
        print('Created Database!')