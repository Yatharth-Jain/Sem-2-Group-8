from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_Name = 'Database.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'My Secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_Name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config["SESSION_PERMANENT"] = False
    # app.config["SESSION_TYPE"] = "sqlalchemy"
    db.init_app(app)

    from .view import view
    from .auth import auth

    from .models import Student, Teacher, Admin, Marks,Years,Courses,Subjects,Sems,ClassForm
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.homepage'
    login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(id):
    #     return Student.query.get(int(id))

    # @login_manager.user_loader
    # def load_user(id):
    #     return Teacher.query.get(int(id))

    @login_manager.user_loader
    def load_user(id):
        if 'name' in session:
            if session['name'] == "student":
                return Student.query.get(int(id))
            elif session['name'] == "admin":
                return Admin.query.get(int(id))
            elif session['name'] == "teacher":
                return Teacher.query.get(int(id))
            else:
                return None
        else:
            return None

    app.register_blueprint(view, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app


def create_database(app):
    if not path.exists('website/'+DB_Name):
        db.create_all(app=app)
        print('Created Database!')
