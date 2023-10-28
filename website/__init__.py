from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from os import path

db = SQLAlchemy()
DB_NAME = "db.SQL"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'bitchimcow' # TODO : change this
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Subject

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    


    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html', user=current_user, Subject=Subject), 404
    
    return app

def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        # give contexte and create the db
        with app.app_context(): 
            db.create_all() # marche plus
        print('Création de la database réussie.')
    else:
        print("Database trouver !")