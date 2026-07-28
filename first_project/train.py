import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, classification_report

# CONFIG
DATA_PATH = 'first_project/data/german.data-numeric'
MODEL_PATH = 'first_project/models/model.pkl'
SEED = 42

# LOAD DATASET
# url del dataset para ver más detalles: https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data
def load_data(data):
    df = pd.read_csv(
        data,
        sep='\s+',
        header=None
    )
    # Asignar nombres a las columnas
    columns = [f'feature_{i}' for i in range(1,25)] + ['target']
    df.columns = columns
    df.columns

    # 1 = buen cliente, 2 = mal cliente
    # Lo pasamos a 0s y 1s
    df['target'] = df['target'].map({1:0, 2:1})

    # Todas las variables están pasadas a numéricas, aunque originalmente fueran categóricas
    # Las dejaremos como numéricas ya que no es el foco de este proyecto
    return df

# SPLIT DATA
def split_data(df):
    X = df.drop('target', axis=1)
    y = df['target']

    return train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y
    )

# BUILD PIPELINE
def build_pipeline():
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', LogisticRegression(max_iter=1000))
    ])
    return pipeline

# TRAIN
def train_model(pipeline, X_train, y_train):
    pipeline.fit(X_train, y_train)
    return pipeline

# EVALUATE
def eval_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    roc_auc = roc_auc_score(y_test, y_prob)
    print('\nModel evaluation:')
    print(f'ROC-AUC: {roc_auc:.4f}')
    print('\nClassification report:')
    print(classification_report(y_test, y_pred))

# SAVE MODEL
def save_model(model, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    print(f'Model was saved at {path}')

# MAIN
def main():
    df = load_data(DATA_PATH)
    X_train, X_test, y_train, y_test = split_data(df)

    pipeline = build_pipeline()
    model = train_model(pipeline, X_train, y_train)

    eval_model(model, X_test, y_test)
    save_model(model, MODEL_PATH)

    print('Training completed successfully.')

if __name__ == '__main__':
    main()