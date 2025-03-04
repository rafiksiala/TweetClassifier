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
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

# ------------------------------------------------------------------------------

# Récupérer la chaîne de connexion Application Insights depuis les variables d'environnement
APP_INSIGHTS_CONNECTION_STRING = os.getenv(
    "APP_INSIGHTS_CONNECTION_STRING",
    "InstrumentationKey=1107ee1d-1bd5-4089-94a4-1dfb765a084a;IngestionEndpoint=https://westeurope-5.in.applicationinsights.azure.com/;LiveEndpoint=https://westeurope.livediagnostics.monitor.azure.com/;ApplicationId=5ad9c7b7-208c-4397-8cc0-1cca49527dbf"
)

# Initialisation du logger pour envoyer les logs à Azure Application Insights
logger = logging.getLogger(__name__)
if not any(isinstance(handler, AzureLogHandler) for handler in logger.handlers) and APP_INSIGHTS_CONNECTION_STRING:
    logger.addHandler(AzureLogHandler(connection_string=APP_INSIGHTS_CONNECTION_STRING))
    logger.setLevel(logging.INFO)
    logger.info("Application Insights connecté avec succès pour FastAPI!")

# ------------------------------------------------------------------------------

# Fonction de nettoyage du texte
def clean_text(w):
    def unicode_to_ascii(s):
        return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

    w = unicode_to_ascii(w.lower().strip())
    w = re.sub(r"([?.!,¿])", r" ", w)
    w = re.sub(r'[" "]+', " ", w)
    w = re.sub(r"[^a-zA-Z0-9?.!,¿]+", " ", w)
    w = re.sub(r'[@#]\w+', '', w)

    return w

# Fonction de prétraitement du texte
def preprocess_text(text, max_len=100):
    with open("vectorizer/vectorizer.pkl", 'rb') as handle:
        vectorizer = pickle.load(handle)

    return vectorizer.transform([clean_text(text)])

# Charger le modèle entraîné
def load_model():
    with open("model/logistic_regression_model.pkl", "rb") as f:
        return pickle.load(f)

# ------------------------------------------------------------------------------

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Tweet Classifier App"}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")

# Charger le modèle
model = load_model()

# Définir la longueur maximale des séquences
max_len = 100

# Fonction pour envoyer un log à Application Insights
def log_prediction(text, prediction, confidence, feedback=None):
    if APP_INSIGHTS_CONNECTION_STRING:
        logger.info(
            "Prediction event",
            extra={
                "custom_dimensions": {
                    "input_text": text,
                    "predicted_sentiment": prediction,
                    "confidence": confidence,
                    "feedback": feedback if feedback else ""
                }
            }
        )


# Classe pour les requêtes de prédiction
class TextRequest(BaseModel):
    text: str

# Endpoint pour la prédiction
@app.post("/predict/")
def predict(request: TextRequest):
    try:
        preprocessed_input = preprocess_text(request.text)
        proba = model.predict_proba(preprocessed_input)[:, 1][0]
        sentiment = 'positif' if proba > 0.5 else 'négatif'
        confidence = max(proba, 1-proba)

        # Log de la prédiction
        log_prediction(request.text, sentiment, confidence)

        return {'sentiment': sentiment, 'confiance': confidence}
    except Exception as e:
        logger.error(f"Erreur lors de la prédiction: {str(e)}")

# ------------------------------------------------------------------------------

# Classe pour les feedbacks utilisateur
class FeedbackRequest(BaseModel):
    text: str
    sentiment: str
    confidence: float
    feedback: str  # "correct" ou "incorrect"

# Endpoint pour stocker le feedback
@app.post("/feedback/")
def feedback(request: FeedbackRequest):
    try:
        # Log du feedback utilisateur
        log_prediction(request.text, request.sentiment, request.confidence, request.feedback)
        logger.info("Feedback envoyé avec succès.")
    except Exception as e:
        logger.error(f"Erreur lors du feedback: {str(e)}")
