import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app

client = TestClient(app)

def test_home():
    """Test que la page d'accueil retourne un message JSON correct"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tweet Classifier API"}

@pytest.mark.parametrize("text, expected_sentiment", [
    ("This airline is a nightmare. Never flying again", "négatif"),
    ("The service was great. The best airline", "positif"),
])
def test_predict_sentiment(text, expected_sentiment):
    """Teste la prédiction du sentiment pour différents types de texte"""
    response = client.post("/predict/", json={"text": text})
    assert response.status_code == 200
    json_data = response.json()
    assert "sentiment" in json_data
    assert json_data["sentiment"] == expected_sentiment

def test_predict_response_content():
    """Vérifie que la réponse contient bien 'sentiment' et 'probability' avec une probabilité valide"""
    response = client.post("/predict/", json={"text": "text"})
    assert response.status_code == 200
    json_data = response.json()
    assert "sentiment" in json_data
    assert "probability" in json_data
    assert 0.5 <= json_data["probability"] <= 1.0

def test_predict_missing_text():
    """Vérifie que l'API retourne une erreur 422 si le texte est absent"""
    response = client.post("/predict/", json={})
    assert response.status_code == 422

def test_predict_empty_text():
    """Teste l'envoi d'un texte vide et vérifie que l'API renvoie un sentiment valide"""
    response = client.post("/predict/", json={"text": ""})
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["sentiment"] in ["positif", "négatif"]

def test_predict_long_text():
    """Teste un texte très long pour s'assurer que l'API ne crash pas"""
    long_text = "good " * 2000
    response = client.post("/predict/", json={"text": long_text})
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["sentiment"] in ["positif", "négatif"]
