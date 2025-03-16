# Application de Prédiction de Sentiments

## Objectif du Projet
Ce projet vise à développer une **API de prédiction de sentiments** pour analyser le ton des tweets. Il repose sur la comparaison de plusieurs approches de modélisation NLP afin d’identifier la plus performante, suivie du déploiement du modèle optimisé, garantissant le meilleur équilibre entre **performance, rapidité d'exécution et coût opérationnel**.

- **Modèle sur mesure simple** : Régression Logistique avec TF-IDF
- **Modèle sur mesure avancé** : LSTM avec embeddings
- **Modèle avancé BERT** : Fine-tuning d’un modèle BERT
- **Tracking et gestion des modèles** avec **MLFlow**
- **Déploiement continu** via **GitHub Actions**
- **Monitoring en production** via **Azure Application Insights**

## Structure du Projet

```
📂 tweet_classifier_app-main/
├── 📜 .gitignore
├── 📜 main.py              # API FastAPI pour la prédiction et le feedback
├── 📜 requirements.txt      # Liste des dépendances
├── 📜 startup.sh            # Script de lancement de l'API
├── 📂 model/                # Contient le modèle entraîné et le tokenizer
│   ├── lstm_model.keras
│   ├── tokenizer.pkl
├── 📂 tests/                # Contient les tests unitaires pour valider les fonctionnalités de l'API
│   ├── test_main.py
├── 📂 .github/workflows/    # Pipeline CI/CD avec GitHub Actions
│   ├── main_tweet-classifier-app.yml
├── notebook.ipynb            # Notebook de modélisation et suivi d’expérimentations
```

## Installation & Lancement
### 1️⃣ Cloner le projet
```bash
git clone https://github.com/rafiksiala/tweet_classifier_app.git
cd tweet_classifier_app
```

### 2️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3️⃣ Lancer l’API et l’interface utilisateur

1. **Lancer l’API avec Uvicorn**

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```  
3. **Tester les prédictions**

   - Via l’interface interactive FastAPI (Swagger UI) : (`http://127.0.0.1:8000/docs`)

   - Via curl :
   ```bash
      curl -X 'POST' 'http://127.0.0.1:8000/predict/' \
        -H 'Content-Type: application/json' \
        -d '{"text": "test"}'
    ```
4. **Déploiement sur le cloud (Azure Web Apps)**

   L’API est déployée sur Azure Web Apps et tourne sur le port 8000.

   Elle est accessible publiquement à l’adresse : 📍 https://tweet-classifier-app.azurewebsites.net/

   L’interface Swagger pour tester les endpoints est disponible ici : 📍 https://tweet-classifier-app.azurewebsites.net/docs


## Endpoints de l'API
| Méthode | Endpoint         | Description |
|---------|----------------|-------------|
| POST    | `/predict`     | Envoie un tweet et retourne la prédiction du sentiment |
| POST    | `/feedback`    | Enregistre le feedback de l’utilisateur sur la prédiction |

## Packages Utilisés

Le projet repose sur plusieurs bibliothèques essentielles, avec leurs versions spécifiées dans le fichier **`requirements.txt`** pour garantir la reproductibilité.  

- **Framework Web & API** : `FastAPI`, `uvicorn`, `gunicorn`, `httpx`
- **Manipulation des données** : `numpy`, `pandas`, `scikit-learn`
- **Machine Learning & NLP** : `tensorflow`, `keras`
- **Gestion des modèles & logs** : `MLFlow`
- **Monitoring & Observabilité** : `opencensus-ext-azure`, `opencensus`, `opencensus-ext-logging`, `opencensus-ext-flask`, `opencensus-ext-requests`
- **Tests et validation** : `pytest`

La version de Python utilisée pour ce projet est **`Python 3.11.11`**.

## Déploiement Automatisé (CI/CD)
Le projet intègre un **pipeline CI/CD avec GitHub Actions** qui permet :
- **Exécution automatique des tests unitaires** avec pytest à chaque commit.
- **Déploiement automatique** de l’API et de l’interface utilisateur sur un service Cloud.
- **Surveillance en production** avec **Azure Application Insights** pour remonter les erreurs.

## Suivi des Performances en Production
- **MLFlow** est utilisé pour tracker les modèles et comparer leurs performances.
- **Azure Application Insights** détecte les tweets mal prédits et déclenche des alertes.
- Un **système d’alerte** est configuré pour envoyer un e-mail/SMS en cas de problème.
