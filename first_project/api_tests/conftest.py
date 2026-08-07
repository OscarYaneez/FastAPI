import pytest
from first_project.first_api import customers, Customer

@pytest.fixture(autouse=True)
def reset_customers():

    customers.clear()

    customers[1] = Customer(
        name='Oscar',
        age=27,
        income=30000
    )