Credit Risk Prediction API

A complete Machine Learning and REST API project built with Python, Scikit-learn and FastAPI and Docker.

This project covers the end-to-end development of a credit risk prediction application, from data preprocessing and model training to API development, automated testing and containerization.

The trained Machine Learning model is exposed through a REST API that supports credit risk predictions and customer management operations.

------------------------------------------------------

Project Overview

The main objective of this project is to build a simple but complete credit risk prediction system based on the German Credit dataset.

The project is divided into three main components:

1. Machine Learning pipeline
-  Exploratory Data Analysis (EDA)
-  Data preprocessing
-  Train/test split
-  Feature scaling
-  Logistic Regression model training
-  Model evaluation
-  Model persistence using Joblib

2. FastAPI application
-  Customer management endpoints
-  Machine Learning prediction endpoint
-  Pydantic data validation
-  Structured API responses
-  Logging
-  Exception handling
-  Automated API tests
-  Test fixtures
-  Code coverage analysis

3. Docker Containerization
- Production-ready Docker image
- Non-root user execution
- Separate Docker image for automated testing
- Docker Compose configuration
- Production and testing environments

------------------------------------------------------

Machine Learning

The current model is a Logistic Regression classifier.

Model evaluation results:
- ROC-AUC: 0.7926
- Accuracy: 0.77

------------------------------------------------------

FastAPI

The trained model is exposed through a REST API built with FastAPI.

The API provides endpoints for customer management as well as an endpoint for Machine Learning predictions.

Main endpoints (Method, Endpoint, Description)

-  GET	/customers	Retrieve all customers
-  GET	/customers/{customer_id}	Retrieve a specific customer
-  POST	/customers/{customer_id}	Create a new customer
-  PUT	/customers/{customer_id}	Update an existing customer
-  DELETE	/customers/{customer_id}	Delete a customer
-  GET	/customers-by-income	Retrieve customers above a given income
-  POST	/predict	Predict the credit risk of a customer using the trained model

Once the application is running, the API documentation can be explored through:

http://localhost:8000/docs

------------------------------------------------------
Machine Learning Prediction Endpoint

The /predict endpoint receives customer features and uses the persisted Machine Learning pipeline to generate a prediction.

Example request:

{
  "features": [1,6,4,12,5,5,3,4,1,67,3,2,2,1,2,1,1,1,1,1,1,1,1,1]
}

Example response:

{
  "prediction": 0,
  "probability": 0.18,
  "risk_level": "low"
}

The endpoint returns:

-  prediction → predicted class
-  probability → estimated probability of bad credit risk
-  risk_level → business-oriented interpretation of the prediction probability

------------------------------------------------------
API Testing

The API is tested using pytest and FastAPI's TestClient. The test suite currently contains 14 tests covering different API behaviours.

Fixtures are used to provide a controlled state for the API during testing and prevent individual tests from interfering with each other.

Tests can be executed locally or inside a dedicated Docker container.

------------------------------------------------------
Docker

The application includes separate Docker configurations for production and testing.


Production environment

The production image:
- Uses Python 3.12 Slim as its base image.
- Installs only production dependencies.
- Runs the application as a non-root user (appuser).
- Includes only the files required to serve predictions.

Build and start the application using Docker Compose:

docker compose up -d --build

The API will be available at:

http://localhost:8000

Interactive documentation:

http://localhost:8000/docs


Testing environment

A separate Docker image is provided for running the automated test suite.

Execute the tests using:

docker compose --profile test run --build --rm test

This command builds the testing image, runs the test suite and removes the temporary test container afterwards.

The current test suite contains 14 tests.

------------------------------------------------------
Running the Project Locally

Docker is the recommended way to run the application, but it can also be executed directly in a Python environment.

1. Clone the repository
   
git clone <repository-url>

cd FastAPI

2. Create and activate a virtual environment

For example, using Conda:

conda create -n fastapidocker python=3.12

conda activate fastapidocker

3. Install dependencies
   
pip install -r requirements.txt

4. Run the API

From the project root:

uvicorn first_project.first_api:app --reload

The API will be available at:

http://localhost:8000

Interactive documentation:

http://localhost:8000/docs

5. Run the tests
 
python -m pytest -v

6. Run tests with coverage
   
coverage run -m pytest

coverage report -m

------------------------------------------------------
Technologies

The project currently uses:

Machine Learning
-  Python
-  NumPy
-  Pandas
-  Scikit-learn
-  Joblib

API
-  FastAPI
-  Pydantic
-  Uvicorn

Testing
-  Pytest
-  FastAPI TestClient
-  HTTPX
-  Coverage.py

Version Control
-  Git
-  GitHub

Containerization
- Docker
- Docker Compose
