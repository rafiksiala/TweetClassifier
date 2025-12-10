# **Sentiment Prediction Application**

## **Project Objective**

This project aims to develop a **sentiment prediction API** to analyse the tone of tweets. It relies on comparing several NLP modelling approaches to identify the most performant one, followed by deploying the optimised model to ensure the best balance between **accuracy, execution speed, and operational cost**.

* **Simple custom model:** Logistic Regression with TF-IDF
* **Advanced custom model:** LSTM with embeddings
* **Advanced BERT model:** Fine-tuning a BERT model
* **Model tracking and management** using **MLFlow**
* **Continuous deployment** via **GitHub Actions**

---

## **Project Structure**

```
📂 tweet_classifier_app-main/
├── 📜 .gitignore
├── 📜 main.py              # FastAPI used for prediction and feedback
├── 📜 requirements.txt      # List of dependencies
├── 📜 startup.sh            # Script to launch the API
├── 📂 model/                # Contains the trained model and tokenizer
│   ├── lstm_model.keras
│   ├── tokenizer.pkl
├── 📂 tests/                # Unit tests validating the API functionalities
│   ├── test_main.py
├── 📂 .github/workflows/    # CI/CD pipeline using GitHub Actions
│   ├── main_tweet-classifier-app.yml
├── notebook.ipynb           # Modelling and experiment tracking notebook
```

---

## **Installation & Launch**

### **1️⃣ Clone the project**

```bash
git clone https://github.com/rafiksiala/tweet_classifier_app.git
cd tweet_classifier_app
```

### **2️⃣ Install dependencies**

```bash
pip install -r requirements.txt
```

### **3️⃣ Launch the API and the user interface**

#### **1. Start the API with Uvicorn**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### **2. Test predictions**

* Via the interactive FastAPI interface (Swagger UI):
  👉 `http://127.0.0.1:8000/docs`

* Via curl:

```bash
curl -X 'POST' 'http://127.0.0.1:8000/predict/' \
  -H 'Content-Type: application/json' \
  -d '{"text": "test"}'
```

#### **3. Cloud Deployment (Azure Web Apps)**

* The API is deployed on Azure Web Apps and runs on port 8000.

* Public URL:
  📍 [https://tweet-classifier-app.azurewebsites.net/](https://tweet-classifier-app.azurewebsites.net/)

* Swagger interface for endpoint testing:
  📍 [https://tweet-classifier-app.azurewebsites.net/docs](https://tweet-classifier-app.azurewebsites.net/docs)

---

## **API Endpoints**

| Method | Endpoint    | Description                                       |
| ------ | ----------- | ------------------------------------------------- |
| POST   | `/predict`  | Sends a tweet and returns the predicted sentiment |
| POST   | `/feedback` | Stores user feedback on the prediction            |

---

## **Packages Used**

The project relies on several essential libraries, with versions specified in the **`requirements.txt`** file to guarantee full reproducibility.

* **Web Framework & API:** `FastAPI`, `uvicorn`, `gunicorn`, `httpx`
* **Data Manipulation:** `numpy`, `pandas`, `scikit-learn`
* **Machine Learning & NLP:** `tensorflow`, `keras`
* **Model & Log Management:** `MLFlow`
* **Testing:** `pytest`

The Python version used for this project is **`Python 3.11.11`**.

---

## **Automated Deployment (CI/CD)**

The project integrates a **CI/CD pipeline with GitHub Actions**, enabling:

* **Automatic execution of unit tests** with pytest on every commit
* **Automatic deployment** of the API to a Cloud service

---

## **Performance Tracking**

* **MLFlow** is used to track models and compare their performance over time.
