import joblib

model = joblib.load("first_project/models/model.pkl")

sample = [[1,6,4,12,5,5,3,4,1,67,3,2,2,1,2,1,1,1,1,1,1,1,1,1]]

print(model.predict(sample))
print(model.predict_proba(sample))