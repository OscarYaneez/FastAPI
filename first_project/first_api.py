from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import os
import numpy as np
import pandas as pd
import logging

class Customer(BaseModel):
    name: str
    age: int
    income: int

class CustomerRisk(Customer):
    risk_level: str

class ModelInput(BaseModel):
    features: list[float] = Field(
        min_length=24,
        max_length=24
    )

class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    risk_level: str

# Configuración y creación del logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Importamos nuestro modelo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'model.pkl')
model = joblib.load(MODEL_PATH)
logger.info('Model loaded successfully')

# Creamos el objeto FastAPI, la API como tal
app = FastAPI()

# Base de datos
customers = {
  1: Customer(
    name="Oscar",
    age= 26,
    income=30000
  )
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
    logger.info('Data of all customers requested.')
    return customers

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    logger.info(f'Data of customer {customer_id} requested.')
    if customer_id not in customers:
        raise HTTPException(status_code=404, detail='Customer not found')
    else:
        return customers.get(customer_id)
    
@app.post("/customers/{customer_id}")
def create_customer(customer_id: int, customer: Customer):
    logger.info(f'Creation of customer {customer_id} requested.')
    if customer_id in customers:
        raise HTTPException(status_code=400, detail= 'Customer already exists')
    else:
        customers[customer_id] = customer
        risk = calculate_risk(customer.income)
        return CustomerRisk(**customer.model_dump(), risk_level=risk)
        
@app.put('/customers/{customer_id}')
def update_customer(customer_id: int, customer: Customer):
    logger.info(f'Update of customer {customer_id} requested.')
    if customer_id not in customers:
        raise HTTPException(status_code=404, detail='Customer not found')
    else:
        customers[customer_id]= customer
        return customers.get(customer_id)
    
@app.delete('/customers/{customer_id}')
def delete_customer(customer_id: int):
    logger.info(f'Deletion of customer {customer_id} requested.')
    if customer_id not in customers:
        raise HTTPException(status_code=404, detail='Customer not found')
    else:
        del customers[customer_id]
        return {"message": "Customer deleted successfully"}
    
@app.get('/customers-by-income')
def get_customers_by_income(min_income: int):
    logger.info(f'Requesting customers with income >= {min_income}.')
    filtered_customers = {
        customer_id: customer 
        for customer_id, customer in customers.items() 
        if customer.income >= min_income
        }
    if not filtered_customers:
        raise HTTPException(status_code=404, detail='No customers found')
    return filtered_customers

@app.post('/predict', response_model=PredictionResponse)
def predict(input_data: ModelInput):
    logger.info('Prediction request received.')
    columns = [f'feature_{i}' for i in range(1,25)]
    data = pd.DataFrame(
        [input_data.features],
        columns=columns
    )

    prediction = int(model.predict(data)[0])
    probability = float(model.predict_proba(data)[0][1])

    risk = get_risk(probability)

    logger.info(
        f'Prediction = {prediction}, '
        f'Probability = {probability:.4f}, '
        f'Risk Level = {risk}'
    )

    return PredictionResponse(
        prediction=prediction,
        probability=probability,
        risk_level=risk
    )