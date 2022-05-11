from flask import Blueprint, jsonify, request, make_response, abort

from app import db
from app.models.cars import Car

# Here is an alternative to the below lines; can put the 
# url_prefix and then an empty string in the route; makes it
# less prone to error
#cars_bp = Blueprint("cars", __name__, url_prefix="/cars")
#@cars_bp.route("", methods=["GET"])

# "cars" is the name of the blueprint; not super important but will be useful in different error messages/debugging
cars_bp = Blueprint("cars", __name__, url_prefix="/cars") #__name__ is required for Flask to "do its magic"
# we can also add an optional parameter above saying url_prefix="/cars"
# so that the route below can be an empty string; creates less room for error

@cars_bp.route("", methods=["POST"])
def create_car():
    request_body = request.get_json()

    #do not need to include id here since id is automatically generated for us
    new_car = Car(
        driver_id=request_body["driver_id"],
        #team=request_body["team"],
        mass_kg=request_body["mass_kg"]
    )

    db.session.add(new_car)
    db.session.commit()

    return {"id": new_car.id}, 201

@cars_bp.route("", methods=["GET"])
def get_all_cars():
    # for one param only:
    # mass_kg_query = request.args.get("mass_kg")
    # if mass_kq_query:
    #     cars = Car.query.filter_by(mass_kg=mass_kg_query)
    # else:
    #     cars = Car.query.all()

    # params = request.args #params will be a dictionary here

    # if "driver" in params and "team" in params:
    #     driver_name = params["driver"]
    #     team_name = params["team"]
    #     cars = Car.query.filter_by(driver=driver_name, team=team_name)
    # elif "driver" in params:
    #     driver_name = params["driver"]
    #     cars = Car.query.filter_by(driver=driver_name)
    # elif "team" in params:
    #     team_name = params["team"]
    #     cars = Car.query.filter_by(team=team_name)
    # elif "mass_kg" in params:
    #     mass_kg_value = params["mass_kg"]
    #     cars = Car.query.filter_by(mass_kg=mass_kg_value)
    # else:
    cars = Car.query.all()

    response = []
    for car in cars:
        response.append(car.to_dict())
    
    return jsonify(response)

# adding a decorator above a function changes what your function does
# @cars_bp.route("/cars", methods=["GET"]) #this decorator tells flask this function will be handling a route
# def get_all_cars():
#     response = []
#     for car in cars:
#         response.append(
#             {
#                 "id": car.id,
#                 "driver": car.driver,
#                 "team": car.team,
#                 "mass_kg": car.mass_kg
#             }
#         )
#     return jsonify(response) #jsonify converts our lists/dictionaries to json objects


# @cars_bp.route("/cars/<car_id>", methods=["GET"])
# def get_one_car(car_id): #the car_id parameter here needs to match the car_id in <angle brackets> in the line above
#     try:
#         car_id = int(car_id)
#     except ValueError:
#         return jsonify({"msg": f"Invalid car id: '{car_id}'. ID must be an integer."}), 400

#     chosen_car = None
#     for car in cars:
#         if car.id == car_id:
#             chosen_car = {
#                 "id": car.id,
#                 "driver": car.driver,
#                 "team": car.team,
#                 "mass_kg": car.mass_kg
#                 }
#     if chosen_car is None:
#         return jsonify({"msg": f"Could not find car with id {car_id}"}), 404

#     return jsonify(chosen_car), 200 
#     # by default, flask sends back a 200, so adding this is not necessary, but you can explicitly put 200 if you'd like

def get_car_or_abort(car_id):
    try:
        car_id = int(car_id)
    except ValueError:
        return abort(make_response(jsonify({'msg': f"Invalid car id: '{car_id}'. ID must be an integer"}), 400))
    
    chosen_car = Car.query.get(car_id) #"get" only works with primary key, otherwise have to filter a different way
    
    if chosen_car is None:
        return abort(make_response(jsonify({"msg": f"Could not find car with id {car_id}"}), 404))

    return chosen_car

@cars_bp.route("/<car_id>", methods=["GET"])
def get_one_car(car_id):
    # try:
    #     car_id = int(car_id)
    # except ValueError:
    #     return jsonify({'msg': f"Invalid car id: '{car_id}'. ID must be an integer"}), 400
    
    # chosen_car = Car.query.get(car_id) #"get" only works with primary key, otherwise have to filter a different way
    
    # if chosen_car is None:
    #     return jsonify({"msg": f"Could not find car with id {car_id}"}), 404
    chosen_car = get_car_or_abort(car_id)

    chosen_car = {
        "id": chosen_car.id,
        "driver": chosen_car.driver,
        "team": chosen_car.team,
        "mass_kg": chosen_car.mass_kg
    }

    return jsonify(chosen_car)

@cars_bp.route("/<car_id>", methods=["PATCH"])
def update_one_car(car_id):
    try:
        car_id = int(car_id)
    except ValueError:
        return jsonify({'msg': f"Invalid car id: '{car_id}'. ID must be an integer"}), 400
    
    request_body = request.get_json()
    
    if "driver" not in request_body or \
        "team" not in request_body or \
        "mass_kg" not in request_body:
        return jsonify({'msg': f"'msg': 'Request must include driver, team, and mass_kg"}), 400

    chosen_car = Car.query.get(car_id) #"get" only works with primary key, otherwise have to filter a different way
    
    if chosen_car is None:
        return jsonify({"msg": f"Could not find car with id {car_id}"}), 404

    chosen_car.driver = request_body["driver"]
    chosen_car.team = request_body["team"]
    chosen_car.mass_kg = request_body["mass_kg"]

    db.session.commit()

    return jsonify({'msg': f"Successfully replaced car with id {car_id}"})

@cars_bp.route("/<car_id>", methods=["DELETE"])
def delete_one_car(car_id):
    try:
        car_id = int(car_id)
    except ValueError:
        return jsonify({'msg': f"Invalid car id: '{car_id}'. ID must be an integer"}), 400
    
    chosen_car = Car.query.get(car_id)
    
    if chosen_car is None:
        return jsonify({"msg": f"Could not find car with id {car_id}"}), 404
    
    db.session.delete(chosen_car)
    db.session.commit()

    return jsonify({'msg': f"Successfully deleted car with id {car_id}"})
