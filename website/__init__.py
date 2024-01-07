from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hello world'    # for production, you don't wanto share this secret key with anybody. 
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note   # we import the models file, so that it defines these those classes for us (user, notes), then we can create our databse.

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'     # where do we need to go or redirect us when the user is not not login? login page.
    login_manager.init_app(app)                 # tell the manager which app that we are using.

    @login_manager.user_loader                  # this is telling flask how we load a user
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
