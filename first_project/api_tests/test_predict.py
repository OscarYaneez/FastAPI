from fastapi.testclient import TestClient
from first_project.first_api import app

client = TestClient(app)

def test_get_prediction():

    response = client.post(
        '/predict',
        json={
            'features':[
                1,6,4,12,5,5,3,4,1,67,3,2,
                2,1,2,1,1,1,1,1,1,1,1,1
                ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert 'prediction' in data
    assert 'probability' in data
    assert 'risk_level' in data

    assert isinstance(data['prediction'], int)
    assert isinstance(data['probability'], float)
    assert isinstance(data['risk_level'], str)

def test_get_prediction_invalid_number_of_features():

    response = client.post(
            '/predict',
            json={
                'features':[
                    1,6,4,12,5,5,3,4,1,67,3,2,
                    2,1,2,1,1,1,1,1,1,1,1
                    ]
            }
        )

    assert response.status_code == 422

def test_get_prediction_invalid_feature_type():

    response = client.post(
            '/predict',
            json={
                'features':[
                    'invalid',6,4,12,5,5,3,4,1,67,3,2,
                    2,1,2,1,1,1,1,1,1,1,1,1
                    ]
            }
        )

    assert response.status_code == 422