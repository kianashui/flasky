from app.models.cars import Car

def test_get_all_cars_with_empty_db_returns_empty_list(client):
    response = client.get('/cars')
    response_body = response.get_json()
    
    assert response.status_code == 200
    assert response_body == []

def test_get_one_car_with_populated_db_returns_car_json(client, seven_cars):
    response = client.get('/cars/1')
    response_body = response.get_json()

    expected_response_body = {
        "id": 1,
        "driver": "Danny Ric",
        "team": "McLaren",
        "mass_kg": 800
    }

    assert response.status_code == 200
    assert response_body == expected_response_body

def test_get_all_cars_with_populated_db_returns_populated_list(client, seven_cars):
    response = client.get('/cars')
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 7

def test_post_one_car_creates_car_in_db(client):
    response = client.post('/cars', json = {
        "driver": "driver name 8",
        "team": "McLaren",
        "mass_kg": 700
    })
    response_body = response.get_json()

    assert response.status_code == 201
    #since the id is autoincremented, don't use this because the id MIGHT not be 1
    #assert response_body == {"id": 1}
    assert "id" in response_body

    cars = Car.query.all()
    assert len(cars) == 1
    assert cars[0].driver == "driver name 8"
    assert cars[0].team == "McLaren"
    assert cars[0].mass_kg == 700

def test_get_one_car_with_empty_db_returns_404(client):
    response = client.get('/cars/1')

    assert response.status_code == 404

def test_get_non_existing_car_with_populated_db_returns_404(client, seven_cars):
    response = client.get('cats/100')
    assert response.status_code == 404