# Application de Prédiction de Sentiments

## 📖 Objectif du Projet
Ce projet vise à développer une **API de prédiction de sentiments** pour analyser le ton des tweets. L'objectif est d'expérimenter différentes approches de modélisation NLP et d'intégrer une démarche **MLOps** complète.

- **Modèle sur mesure simple** : Régression Logistique avec TF-IDF
- **Modèle sur mesure avancé** : LSTM avec embeddings
- **Modèle avancé BERT** : Fine-tuning d’un modèle BERT
- **Tracking et gestion des modèles** avec **MLFlow**
- **Déploiement continu** via **GitHub Actions**
- **Interface de test utilisateur** avec **Streamlit**
- **Monitoring en production** via **Azure Application Insights**

## 🏗️ Structure du Projet

```
📂 tweet_classifier_app-main/
├── 📜 .gitignore
├── 📜 app.py               # Interface utilisateur avec Streamlit
├── 📜 main.py              # API FastAPI pour la prédiction et le feedback
├── 📜 requirements.txt      # Liste des dépendances
├── 📜 startup.sh            # Script de lancement (API + Streamlit)
├── 📂 model/                # Contient les modèles entraînés (Logistic Regression, LSTM, BERT)
│   ├── logistic_regression_model.pkl
├── 📂 vectorizer/           # Contient le vectorizer TF-IDF
│   ├── vectorizer.pkl
├── 📂 tests/                # Contient les tests unitaires pour valider les fonctionnalités de l'API
│   ├── test_main.py
├── 📂 .github/workflows/    # Pipeline CI/CD avec GitHub Actions
│   ├── main_tweet-classifier-app.yml
```

## 🚀 Installation & Lancement
### 1️⃣ Cloner le projet
```bash
git clone <repo_url>
cd tweet_classifier_app-main
```

### 2️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3️⃣ Lancer l’API et l’interface utilisateur
Le lancement se fait via **startup.sh** qui démarre à la fois l'API et l'interface Streamlit.

```bash
bash startup.sh
```

Ce script exécute :
- **FastAPI avec Gunicorn** en arrière-plan sur le port **8001**
- **Streamlit** sur le port **8000**

## 🔗 Endpoints de l'API
| Méthode | Endpoint         | Description |
|---------|----------------|-------------|
| POST    | `/predict`     | Envoie un tweet et retourne la prédiction du sentiment |
| POST    | `/feedback`    | Enregistre le feedback de l’utilisateur sur la prédiction |

## 📦 Packages Utilisés
Le projet repose sur plusieurs bibliothèques essentielles :

- **Framework Web & API** : `FastAPI`, `uvicorn`, `gunicorn`, `httpx`
- **Manipulation des données** : `numpy`, `pandas`, `scikit-learn`
- **Machine Learning & NLP** : `transformers`, `torch`
- **Interface utilisateur** : `streamlit`
- **Gestion des modèles & logs** : `MLFlow`
- **Monitoring & Observabilité** : `opencensus-ext-azure`, `opencensus`, `opencensus-ext-logging`, `opencensus-ext-flask`, `opencensus-ext-requests`
- **Tests et validation** : `pytest`, `pydantic`

## 🔄 Déploiement Automatisé (CI/CD)
Le projet intègre un **pipeline CI/CD avec GitHub Actions** qui permet :
- **Exécution automatique des tests unitaires** avec pytest à chaque commit.
- **Déploiement automatique** de l’API et de l’interface utilisateur sur un service Cloud.
- **Surveillance en production** avec **Azure Application Insights** pour remonter les erreurs.

## 📊 Suivi des Performances en Production
- **MLFlow** est utilisé pour tracker les modèles et comparer leurs performances.
- **Azure Application Insights** détecte les tweets mal prédits et déclenche des alertes.
- Un **système d’alerte** est configuré pour envoyer un e-mail/SMS en cas de problème.
