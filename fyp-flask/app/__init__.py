from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
import os

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def init_db():
    """
    : Create and Initialize Database and Tables before the very first request comesin
    """
    db.create_all()

def init_app():
    app = Flask (__name__, instance_relative_config=False)
    CORS(app)
    app.config.from_object ('config.Config')
    app.config.update(SECRET_KEY=os.urandom(24))
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for spark parts of app
    from .process import process as process_blueprint
    app.register_blueprint(process_blueprint)
    
    return app