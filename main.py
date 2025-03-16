from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

import uvicorn

import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

from functools import lru_cache

import pandas as pd
import numpy as np

import unicodedata
import pickle
import json
import re
import os

# ------------------------------------------------------------------------------

# Récupérer la chaîne de connexion Application Insights depuis les variables d'environnement
APP_INSIGHTS_CONNECTION_STRING = os.getenv(
    "APP_INSIGHTS_CONNECTION_STRING",
    "InstrumentationKey=1107ee1d-1bd5-4089-94a4-1dfb765a084a;IngestionEndpoint=https://westeurope-5.in.applicationinsights.azure.com/;LiveEndpoint=https://westeurope.livediagnostics.monitor.azure.com/;ApplicationId=5ad9c7b7-208c-4397-8cc0-1cca49527dbf"
)

# Initialisation du logger pour envoyer les logs à Azure Application Insights
logger = logging.getLogger(__name__)

logger.handlers.clear()
logger.propagate = False

if not any(isinstance(handler, AzureLogHandler) for handler in logger.handlers) and APP_INSIGHTS_CONNECTION_STRING:
    logger.addHandler(AzureLogHandler(connection_string=APP_INSIGHTS_CONNECTION_STRING))

logger.setLevel(logging.INFO)
logger.info("Application Insights connecté avec succès pour FastAPI!")

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

# Fonction pour envoyer un log à Application Insights

def log_prediction(text, prediction, probability):
    if APP_INSIGHTS_CONNECTION_STRING:
        logger.info("Prediction envoyé avec succès", extra={
            "custom_dimensions": {
                "input_text": text,
                "predicted_sentiment": prediction,
                "probability": probability
            }})

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

        # Log de la prediciton
        log_prediction(request.text, sentiment, probability)

        return {'sentiment': sentiment, 'probability': probability}

    except Exception as e:
        logger.error(f"Erreur lors de la prédiction: {str(e)}")

# ------------------------------------------------------------------------------

def log_feedback(text, prediction, probability, feedback):
    if APP_INSIGHTS_CONNECTION_STRING:
        message = "Tweet correctement prédit" if feedback=="correct" else "Tweet mal prédit"
        logger.info(message, extra={
            "custom_dimensions": {
                "input_text": text,
                "predicted_sentiment": prediction,
                "probability": probability,
                "feedback": feedback
            }})

# Classe pour les feedbacks utilisateur
class FeedbackRequest(BaseModel):
    text: str
    sentiment: str
    probability: float
    feedback: str  # "correct" ou "incorrect"

# Endpoint pour stocker le feedback
@app.post("/feedback/")
def feedback(request: FeedbackRequest):
    try:
        # Log du feedback utilisateur
        log_feedback(request.text, request.sentiment, request.probability, request.feedback)

    except Exception as e:
        logger.error(f"Erreur lors du feedback: {str(e)}")
