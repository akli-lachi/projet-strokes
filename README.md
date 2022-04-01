# strokes
The project is to predict whether a patient is likely to get stroke

Audit, exploration, et nettoyage des données, Visualisation, Entraînement et évaluation de modèles de machine learning : strokes-ML.py

Déploiement du modèle du projet via une API HTTP REST FastAPI : strokes.py

L'objectif de cette API est de déployer les modèles créés. Les modèles ne sont pas ré-entrainés et nous faisons donc appel à un joblib pour chaque modèle. L'API permet d'interroger les différents modèles. Les utilisateurs pourront interroger l'API pour accéder aux performances de l'algorithme sur les jeux de tests.

La liste d'utilisateurs/mots de passe est la suivante: alice/wonderland, bob/builder, clementine/mandarine

Endpoints :

GET /status

Renvoie 1 si l’API fonctionne.

GET /performance

Cette fonction renvoie les performance d'un modele MODEL : lr (LogisticRegression) / kn (K-Nearest Neighbors) / dt (Decision Tree Classification) / rf (Random Forest Classification)

POST /users/prediction

Cette fonction renvoie les predictions pour un ou plusieurs individus de subir une attaque. Renvoie 1 si la personne est susceptible d'avoir une attaque, 0 sinon.

Example value: [ { "gender": 1, "age": 20, "hypertension": 1, "heart_disease": 0, "ever_married": 1, "urban_residence": 0, "avg_glucose_level": 200, "bmi": 40, "smoking_status": 1 } ]

POST /file/prediction

Cette fonction renvoie les predictions pour un fichier d'individu de subir une attaque. Renvoie 1 si la personne est susceptible d'avoir une attaque, 0 sinon.

Fichier csv entete : id,gender,age,hypertension,heart_disease,ever_married,urban_residence,avg_glucose_level,bmi,smoking_status

Fichier test : Docker\FilePrediction\strokestest.csv

Un container Docker a été créé pour déployer facilement l'API: https://hub.docker.com/repository/docker/ylefe/strokes-api

Une série de tests a été créée pour tester l'API contenairisée (fichier docker-compose.yml)

Un fichier de déploiement ainsi qu'un Service et un Ingress avec Kubernetes permet le déploiement de l'API sur au moins 3 Pods.
