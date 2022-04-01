FROM python:3.8
ADD newstrokes.csv ../Model/minmax_scaler.bin ../Model/rf_model.joblib ../Model/dt_model.joblib ../Model/lr_model.joblib ../Model/kn_model.joblib requirements.txt strokes.py ./
RUN apt-get update && apt-get install python3-pip -y && pip install -r ./requirements.txt
CMD uvicorn strokes:api --reload