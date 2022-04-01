from fastapi import FastAPI, Depends, Header, HTTPException, status, File, UploadFile
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import pandas as pd
import numpy as np
import json
from random import choices
from sklearn import metrics
from sklearn.model_selection import train_test_split
import joblib
from joblib import dump, load

# importation du daset
df = pd.read_csv('newstrokes.csv', sep = ',', header = 0, index_col = 0)

#separation des variables explicatives dans un dataframe X et la variable cible dans y.
X = df.drop("stroke", axis = 1)
y = df.stroke

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

users = {
  "alice": "wonderland",
  "bob": "builder",
  "clementine": "mandarine"
}

class Performance(BaseModel):
    accuracy: str
    precision: str
    recall: str
    f1_score: str
    mcc: str

class Individual(BaseModel):
    gender: int
    age: float
    hypertension: int
    heart_disease: int
    ever_married: int
    urban_residence: int
    avg_glucose_level: float
    bmi: float
    smoking_status: int


api = FastAPI(
    title="Strokes prediction API",
    description="API pour predire si une personne va subir une attaque",
    version="1.0.1",
    openapi_tags=[
    {
        'name': 'Home',
        'description': 'Default functions'
    },
    {
        'name': 'Performance',
        'description': 'Functions that are used to deal with performances'
    },
    {
        'name': 'Prediction',
        'description': 'Functions that are used to deal with predictions'
    }
    ]
)

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    for key, value in users.items():
        if credentials.username==key and credentials.password==value:
            return credentials.username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Basic"},
    )

def get_admin_username(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username=='admin' and credentials.password=='4dm1N':
        return credentials.username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Basic"},
    )

    
@api.get('/status', name='Get API status', tags=['Home'])
def get_status(username: str = Depends(get_current_username)):
    """Cette fonction renvoie 1 si l'API fonctionne.
    """
    return 1

@api.get('/performance', name='Get model performance ', tags=['Performance'])
async def get_performance(model: str, username: str = Depends(get_current_username)):
    """Cette fonction renvoie les performance d'un modele\n
        MODEL : lr (LogisticRegression) / kn (K-Nearest Neighbors) / dt (Decision Tree Classification) / rf (Random Forest Classification)
    """

    global X_test
    global y_test

    try:
        if (model=="lr"):
            mod=load('../Model/lr_model.joblib')
        elif (model=="kn"):
            mod=load('../Model/kn_model.joblib')
        elif (model=="dt"):
            mod=load('../Model/dt_model.joblib')
        elif (model=="rf"):
            mod=load('../Model/rf_model.joblib')

        preds = mod.predict(X_test)
        performance = {
            'accuracy': str(metrics.accuracy_score(y_test, preds)),
            'precision': str(metrics.precision_score(y_test, preds)),
            'recall': str(metrics.recall_score(y_test, preds)),
            'f1_score': str(metrics.f1_score(y_test, preds)),
            'mcc': str(metrics.matthews_corrcoef(y_test, preds))
        }

        return performance 

    except IndexError:
        raise HTTPException(
            status_code=404,
            detail='Unknown Index')
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail='Bad Type'
        )

@api.post('/users/prediction', name='Get stroke prediction for one or more individuals', tags=['Prediction'])
async def get_prediction(model: str, individuals: List[Individual], username: str = Depends(get_current_username)):
    """Cette fonction renvoie les predictions pour un ou plusieurs individus de subir une attaque.\n
       MODEL : lr (LogisticRegression) / kn (K-Nearest Neighbors) / dt (Decision Tree Classification) / rf (Random Forest Classification)
    """
    
    try:
        if (model=="lr"):
            mod=load('../Model/lr_model.joblib')
        elif (model=="kn"):
            mod=load('../Model/kn_model.joblib')
        elif (model=="dt"):
            mod=load('../Model/dt_model.joblib')
        elif (model=="rf"):
            mod=load('../Model/rf_model.joblib')

        individus = []
        for index, individual in enumerate(individuals):
            individu = {
                'id': index,
                'gender': individual.gender,
                'age': individual.age,
                'hypertension': individual.hypertension,
                'heart_disease': individual.heart_disease,
                'ever_married': individual.ever_married,
                'urban_residence': individual.urban_residence,
                'avg_glucose_level': individual.avg_glucose_level,
                'bmi': individual.bmi,
                'smoking_status': individual.smoking_status
            }
            individus.append(individu)
        df = pd.DataFrame(individus)
        df = df.set_index('id')
        scaler=load('../Model/minmax_scaler.bin')
        df = scaler.transform(df)
        pred = mod.predict(df)
        pred_lists = pred.tolist()
        pred_jason = json.dumps(pred_lists)
        return pred_jason

    except IndexError:
        raise HTTPException(
            status_code=404,
            detail='Unknown Index')
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail='Bad Type'
        )

@api.post('/file/prediction', name='Get stroke prediction for individuals by using a file', tags=['Prediction'])
async def get_prediction_file(model: str, csv_file: UploadFile = File(...), username: str = Depends(get_current_username)):
    """Cette fonction renvoie les predictions pour un fichier d'individu de subir une attaque.\n
       MODEL : lr (LogisticRegression) / kn (K-Nearest Neighbors) / dt (Decision Tree Classification) / rf (Random Forest Classification)
    """
    
    try:
        if (model=="lr"):
            mod=load('../Model/lr_model.joblib')
        elif (model=="kn"):
            mod=load('../Model/kn_model.joblib')
        elif (model=="dt"):
            mod=load('../Model/dt_model.joblib')
        elif (model=="rf"):
            mod=load('../Model/rf_model.joblib')
            
        df = pd.read_csv(csv_file.file, sep = ',', header = 0, index_col = 0)
        scaler=load('../Model/minmax_scaler.bin')
        df = scaler.transform(df)
        pred = mod.predict(df)
        pred_lists = pred.tolist()
        pred_jason = json.dumps(pred_lists)
        return pred_jason
            
    except IndexError:
        raise HTTPException(
            status_code=404,
            detail='Unknown Index')
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail='Bad Type'
        )