from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
import numpy as np

class Customer(BaseModel):
    name: str
    age: int
    income: int

class CustomerRisk(Customer):
    risk_level: str

class ModelInput(BaseModel):
    features: list[float]

# Importamos nuestro modelo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'model.pkl')
model = joblib.load(MODEL_PATH)

# Creamos el objeto FastAPI, la API como tal
app = FastAPI()

# Base de datos
customers = {
  1: {
    "name": "Oscar",
    "age": 26,
    "income": 30000
  }
}

# Función para calcular el riesgo del cliente para hacer un campo calculado
def calculate_risk(income):
    if income < 20000:
        return "High"
    elif income < 50000:
        return "Medium"
    else:
        return "Low"

# Función para calcular el riesgo del cliente según la probabilidad estimada por el modelo
def get_risk(prob):
    if prob < 0.3:
        return 'low'
    elif prob < 0.7:
        return 'medium'
    else:
        return 'high'

# Endpoints de la API

@app.get("/customers")
def get_customers():
    return customers

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    if customer_id not in customers:
        raise HTTPException(status_code=404, detail='Customer not found')
    else:
        return customers.get(customer_id)
    
@app.post("/customers/{customer_id}")
def create_customer(customer_id: int, customer: Customer):
    if customer_id in customers:
        raise HTTPException(status_code=400, detail= 'Customer already exists')
    else:
        customers[customer_id] = customer.dict()
        risk = calculate_risk(customer.income)
        return CustomerRisk(**customer.dict(), risk_level=risk)
        
@app.put('/customers/{customer_id}')
def update_customer(customer_id: int, customer: Customer):
    if customer_id not in customers:
        raise HTTPException(status_code=404, detail='Customer not found')
    else:
        customers[customer_id]= customer
        return customers.get(customer_id)
    
@app.delete('/customers/{customer_id}')
def delete_customer(customer_id: int):
    if customer_id not in customers:
        raise HTTPException(status_code=404, detail='Customer not found')
    else:
        del customers[customer_id]
        return {"message": "Customer deleted successfully"}
    
@app.get('/customers-by-income')
def get_customers_by_income(min_income: int):
    filtered_customers = {
        customer_id: customer 
        for customer_id, customer in customers.items() 
        if customer['income'] >= min_income}
    if not filtered_customers:
        raise HTTPException(status_code=404, detail='No customers found')
    return filtered_customers

@app.post('/predict')
def predict(input_data: ModelInput):
    data = np.array(input_data.features).reshape(1, -1)

    prediction = model.predict(data)[0]
    probability = model.predict_proba(data)[0][1]

    risk = get_risk(probability)
    return {
        'prediction': prediction,
        'probability': probability,
        'risk_level': risk
    }