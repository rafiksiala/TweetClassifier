from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

import pandas as pd
import numpy as np

import unicodedata
import uvicorn
import pickle
import json
import re
import os


# ------------------------------------------------------------------------------

# Fonction de nettoyage du texte
def clean_text(w):

    def unicode_to_ascii(s):
        return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

    w = unicode_to_ascii(w.lower().strip())
    w = re.sub(r"([?.!,¿])", r" ", w)
    w = re.sub(r'[" "]+', " ", w)
    w = re.sub(r"[^a-zA-Z0-9?.!,¿]+", " ", w)
    w = re.sub(r'[@#]\w+', '',w)

    return w

# Fonction de prétraitement du texte
def preprocess_text(text, max_len=100):
    with open("vectorizer/vectorizer.pkl", 'rb') as handle:
            vectorizer = pickle.load(handle)

    return vectorizer.transform([clean_text(text)])


def load_model():
    with open("model/logistic_regression_model.pkl", "rb") as f:
        return pickle.load(f)

# ------------------------------------------------------------------------------

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Tweet Classsifier App"}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")

# ------------------------------------------------------------------------------

# Charger le modèle entraîné
model = load_model()

# Définir la longueur maximale des séquences
max_len = 100

class NameRequest(BaseModel):
    name: str

@app.post("/predict/")
def predict(request: NameRequest):
    try:
        preprocessed_input = preprocess_text(request.name)
        proba = model.predict_proba(preprocessed_input)[:, 1][0]
        sentiment = 'positif' if proba > 0.5 else 'négatif'
        return {'sentiment': sentiment, 'confiance': max(proba, 1-proba)}
    except Exception as e:
        return {"error": str(e)}
