import streamlit as st
import requests

# FastAPI tourne en interne sur `127.0.0.1:8001`
API_URL = "http://127.0.0.1:8001/predict/"

st.title("Analyse de Sentiment avec FastAPI et Streamlit")

user_input = st.text_area("Entrez votre texte ici :")

if st.button("Prédire le sentiment"):
    if user_input:
        try:
            response = requests.post(API_URL, json={"name": user_input})
            if response.status_code == 200:
                result = response.json()
                st.write(f"Sentiment : **{result['sentiment']}**")
                st.write(f"Confiance : **{result['confiance']:.2f}**")
            else:
                st.error(f"Erreur {response.status_code} : {response.text}")
        except requests.exceptions.RequestException as e:
            st.error("Impossible de se connecter à l'API.")
            st.text(str(e))
    else:
        st.warning("Veuillez entrer un texte.")
