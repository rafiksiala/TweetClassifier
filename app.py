import streamlit as st
import requests

# Configuration de l'API
API_URL = "https://tweet-classifier-app.azurewebsites.net/api/predict/"

st.title("Analyse de Sentiment avec FastAPI et Streamlit")

user_input = st.text_area("Entrez votre texte ici :")

if st.button("Prédire le sentiment"):
    if user_input:
        response = requests.post(API_URL, json={"name": user_input})
        if response.status_code == 200:
            result = response.json()
            st.write(f"Sentiment : **{result['sentiment']}**")
            st.write(f"Confiance : **{result['confiance']:.2f}**")
        else:
            st.error("Erreur lors de la requête à l'API.")
    else:
        st.warning("Veuillez entrer un texte.")
