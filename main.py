from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

import pandas as pd
import numpy as np

import mlflow

import nltk
from nltk.corpus import stopwords

import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

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

    def clean_stopwords_shortwords(w):
        stopwords_list=stopwords.words('english')
        words = w.split()
        clean_words = [word for word in words if (word not in stopwords_list) and len(word) > 2]
        return " ".join(clean_words)

    w = unicode_to_ascii(w.lower().strip())
    w = re.sub(r"([?.!,¿])", r" ", w)
    w = re.sub(r'[" "]+', " ", w)
    w = re.sub(r"[^a-zA-Z0-9?.!,¿]+", " ", w)
    w = clean_stopwords_shortwords(w)
    w = re.sub(r'[@#]\w+', '',w)

    return w

# Fonction de prétraitement du texte
def preprocess_text(text, max_len=100):

    # Charger le tokenizer entraîné
    with open("tokenizer/tokenizer.pkl", 'rb') as handle:
            tokenizer = pickle.load(handle)

    sequence = tokenizer.texts_to_sequences([clean_text(text)])
    return pad_sequences(sequence, maxlen=max_len)

def load_best_model():
    return mlflow.tensorflow.load_model("model/keras_model_w2v")

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
#best_model = load_best_model()

# Définir la longueur maximale des séquences
max_len = 100

class NameRequest(BaseModel):
    name: str

@app.post("/predict/")
def predict(request: NameRequest):
    try:
        #preprocessed_input = preprocess_text(request.name)
        #prediction = best_model.predict(preprocessed_input)
        #proba = float(prediction[0][0])
        #sentiment = 'positif' if proba > 0.5 else 'négatif'
        #return {'sentiment': sentiment, 'confiance': max(proba, 1-proba)}
        return {'sentiment': 'positif', 'confiance': 1}
    except Exception as e:
        return {"error": str(e)}
