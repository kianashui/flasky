from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(testing=None):
    # __name__ stores the name of the module we're in
    app = Flask(__name__) #creates a new flask object that handles all of these requests/responses

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/hello_cars_development'

    if testing is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('TESTING_SQLALCHEMY_DATABASE_URI')

    db.init_app(app)
    migrate.init_app(app, db)

    from .models.cars import Car
    from .models.drivers import Driver

    from .routes.cars import cars_bp #gets a blueprint
    app.register_blueprint(cars_bp) #tells our app about the blueprint

    from .routes.drivers import drivers_bp
    app.register_blueprint(drivers_bp)
    
    return app #so when flask automatically finds this function, it's able to get the configured app back