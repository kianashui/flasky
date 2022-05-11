from readline import append_history_file
import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.cars import Car

#this fixture sets up our flask app for us so we can do the flask work with a flask app
#so we can send it requests and get responses back and allow us to test our routes
@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()
    
    # this section of code sets up our database then returns our app. lets us use the app
    # when we're done using the app we can add something
    with app.app_context():
        #this will create/instantiate our database, 
        #set up the tables, does db init/db upgrade work for us
        db.create_all()
        yield app #returns app, allowing client to use app
    
    #this chunk will clean up everything that happens in our database
    #we want to start every test with a clean database
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    #sets up this app/client structure so we can write tests for our routes
    return app.test_client()

@pytest.fixture
def seven_cars(app): #having access to the app gives us access to the database
    #don't need to add the id but we want to have control over as much as possible for tests
    #so this allows us to know exactly what the structure of our database is
    car1 = Car(id=1, driver='Danny Ric', team='McLaren', mass_kg=800)
    car2 = Car(id=2, driver='Carlos', team='Ferrari', mass_kg=750)
    car3 = Car(id=3, driver='driver name 3', team='McLaren', mass_kg=700)
    car4 = Car(id=4, driver='driver name 4', team='Mercedes', mass_kg=750)
    car5 = Car(id=5, driver='driver name 5', team='Mercedes', mass_kg=800)
    car6 = Car(id=6, driver='driver name 6', team='Ferrari', mass_kg=750)
    car7 = Car(id=7, driver='driver name 7', team='McLaren', mass_kg=800)

    db.session.add(car1)
    db.session.add(car2)
    db.session.add(car3)
    db.session.add(car4)
    db.session.add(car5)
    db.session.add(car6)
    db.session.add(car7)

    db.session.commit()