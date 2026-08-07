from fastapi.testclient import TestClient
from first_project.first_api import app

client = TestClient(app)

def test_get_all_customers():

    response = client.get('/customers')

    assert response.status_code == 200

    data = response.json()

    assert data['1']['name'] == 'Oscar'
    assert data['1']['age'] == 27
    assert data['1']['income'] == 30000

def test_get_customer_by_id():

    response = client.get('/customers/1')

    assert response.status_code == 200

    data = response.json()

    assert data['name'] == 'Oscar'
    assert data['age'] == 27
    assert data['income'] == 30000

def test_get_customer_by_id_not_found():

    response = client.get('/customers/10')

    assert response.status_code == 404
    assert response.json()['detail'] == 'Customer not found'

def test_create_customer():

    new_customer = {
        "name": "Pedro",
        "age": 30,
        "income": 60000
    }

    response = client.post('/customers/2', json=new_customer)

    assert response.status_code == 200

    data = response.json()

    assert data['name'] == 'Pedro'
    assert data['age'] == 30
    assert data['income'] == 60000
    assert data['risk_level'] == 'Low'

def test_create_existing_customer():

    existing_customer = {
        "name": "Oscar",
        "age": 27,
        "income": 30000
    }

    response = client.post('/customers/1', json=existing_customer)

    assert response.status_code == 400
    assert response.json()['detail'] == 'Customer already exists'

def test_update_customer():

    updated_customer = {
        'name': 'Oscar Updated',
        'age': 28,
        'income': 40000
    }

    response = client.put('/customers/1', json=updated_customer)

    assert response.status_code == 200

    data = response.json()

    assert data['name'] == 'Oscar Updated'
    assert data['age'] == 28
    assert data['income'] == 40000

def test_update_nonexistent_customer():

    updated_customer = {
        'name': 'Nonexistent Customer',
        'age': 35,
        'income': 50000
    }

    response = client.put('/customers/10', json=updated_customer)

    assert response.status_code == 404
    assert response.json()['detail'] == 'Customer not found'

def test_delete_customer():

    response = client.delete('/customers/1')

    assert response.status_code == 200
    assert response.json()['message'] == 'Customer deleted successfully'

def test_delete_nonexistent_customer():
    
    response = client.delete('/customers/10')

    assert response.status_code == 404
    assert response.json()['detail'] == 'Customer not found'

def test_get_customers_by_income():

    response = client.get('/customers-by-income?min_income=25000')

    assert response.status_code == 200

    data = response.json()
    assert len(data) > 0
    assert all(customer['income'] >= 25000 for customer in data.values())

def test_get_customers_by_income_not_found():

    response = client.get('/customers-by-income?min_income=100000')

    assert response.status_code == 404
    assert response.json()['detail'] == 'No customers found'