# from sqlalchemy import PrimaryKeyConstraint
from app import db

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("driver.id"))
    #team = db.Column(db.String)
    mass_kg = db.Column(db.Integer)
    #driver = db.relationship("Driver", back_populates="cars") #Driver here needs to match the class name Driver
    #back_populates variable "cars" needs to match the attribute name under the Driver model
    driver = db.relationship("Driver", backref="cars")

    def to_dict(self):
        return {
            "id": self.id,
            "driver": self.driver.name,
            "team": self.driver.team,
            "mass_kg": self.mass_kg
        }
    
    def to_dict_basic(self):
        return {
            "id": self.id,
            "mass_kg": self.mass_kg
        }

# class Car(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     driver = db.Column(db.String)
#     team = db.Column(db.String)
#     mass_kg = db.Column(db.Integer)


# class Car:
#     def __init__(self, id, driver, team, mass_kg):
#         self.id = id
#         self.driver = driver
#         self.team = team
#         self.mass_kg = mass_kg

# cars = [
#     Car(7, "Sainz", "Ferrari", 795),
#     Car(88, "SHARLES", "Ferrari", 800),
#     Car(4, "Danny Ric", "McLaren", 1138)
# ]