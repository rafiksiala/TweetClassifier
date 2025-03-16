from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

from functools import lru_cache

import pandas as pd
import numpy as np

import unicodedata
import uvicorn
import pickle
import json
import re
import os


# ------------------------------------------------------------------------------

@lru_cache(maxsize=1)
def preprocess_text(text, max_len=100):
    text = text.lower().strip()
    text = re.sub(r'http\S+|www\.\S+', '', text)
    text = re.sub(r'[@#]\w+', '', text)
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    text = re.sub(r"([?.!,¿])", r" ", text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r"[^a-zA-Z0-9]+", " ", text)
    sequence = tokenizer.texts_to_sequences([text])
    return pad_sequences(sequence, maxlen=max_len)

def load_model():
    return tf.keras.models.load_model("model/lstm_model.keras")

def load_tokenizer():
    with open("model/tokenizer.pkl", 'rb') as handle:
        return pickle.load(handle)

# Charger le modèle
model = load_model()

# Charger le tokenisateur
tokenizer = load_tokenizer()

# Définir la longueur maximale des séquences
max_len = 100

# ------------------------------------------------------------------------------

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Tweet Classifier API"}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")

# Classe pour les requêtes de prédiction
class TextRequest(BaseModel):
    text: str

# Endpoint pour la prédiction
@app.post("/predict/")
def predict(request: TextRequest):
    try:
        preprocessed_text = preprocess_text(request.text)

        probability = float(model.predict(preprocessed_text)[0, 0])
        label = 1 if probability >= 0.5 else 0
        probability = max(probability, 1 - probability)
        sentiment = 'positif' if label else 'négatif'

        return {'sentiment': sentiment, 'probability': probability}

    except Exception as e:
        logger.error(f"Erreur lors de la prédiction: {str(e)}")
