from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config


# Initialize the Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    migrate.init_app(app, db)

    # Import and register Blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
