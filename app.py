import streamlit as st
import requests
import logging

# Configuration des URLs de l'API FastAPI
API_URL = "http://127.0.0.1:8000/predict/"
FEEDBACK_URL = "http://127.0.0.1:8000/feedback/"

st.title("Analyse de Sentiment")

# Initialiser st.session_state pour éviter les KeyErrors
if "sentiment" not in st.session_state:
    st.session_state["sentiment"] = None
if "probabitlity" not in st.session_state:
    st.session_state["probabitlity"] = None
if "user_input" not in st.session_state:
    st.session_state["user_input"] = None
if "feedback" not in st.session_state:
    st.session_state["feedback"] = None
if "feedback_sent" not in st.session_state:
    st.session_state["feedback_sent"] = False  # Variable pour cacher les boutons après l'envoi


st.markdown(
    """
    <style>
        textarea {
            width: 100% !important;
            height: 100% !important;
            font-size: px;
            border-radius: 10px;
            border: 2px solid #ccc;
            background-color: #f9f9f9;
            color: #333;
            transition: all 0.3s ease-in-out;
        }

        /* Effet au focus (quand l'utilisateur clique) */
        textarea:focus {
            border-color: #4CAF50 !important;
            box-shadow: 0px 0px 10px rgba(76, 175, 80, 0.3);
            background-color: white;
            outline: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

user_input = st.text_area(" ", placeholder="Écrivez votre texte ici ...", height=150)

# Bouton pour prédire le sentiment
if st.button("Prédire le sentiment"):
    if user_input:
        try:
            response = requests.post(API_URL, json={"text": user_input})
            if response.status_code == 200:
                result = response.json()
                st.session_state["sentiment"] = result.get("sentiment", None)
                st.session_state["probabitlity"] = result.get("probabitlity", 0)
                st.session_state["user_input"] = user_input
                st.session_state["feedback"] = None  # Reset du feedback pour réafficher les boutons
                st.session_state["feedback_sent"] = False  # Réaffichage des boutons
                st.rerun()  # Recharge l'interface pour afficher le résultat
            else:
                st.error(f"Erreur {response.status_code} : {response.text}")
        except requests.exceptions.RequestException as e:
            st.error("Impossible de se connecter à l'API.")

# Affichage du résultat de la prédiction
if st.session_state["sentiment"]:
    emoji = "😊" if st.session_state["sentiment"] == "positif" else "😠"

    st.markdown(
        """
        <style>
            .result-container {
                display: flex;
                align-items: center;
                justify-content: space-between;
                background-color: white;
                padding: 15px 20px;
                border-radius: 10px;
                border: 3px solid #ddd;
                box-shadow: 2px 2px 15px rgba(0, 0, 0, 0.1);
                width: 67%;
                margin: 0px 0px 20px 0px;
                transition: all 0.3s ease-in-out;
            }

            .result-container:hover {
                box-shadow: 3px 3px 20px rgba(0, 0, 0, 0.2);
            }

            .result-text {
                font-size: 24px;
                font-weight: bold;
                color: black;
                margin: 0;
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .result-probabitlity {
                font-size: 18px;
                font-weight: normal;
                color: #555;
            }

            /* Changement de couleur selon le sentiment */
            .positive {
                border-color: #4CAF50;
                background-color: #E8F5E9;
            }

            .negative {
                border-color: #F44336;
                background-color: #FFEBEE;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Déterminer la classe CSS en fonction du sentiment
    sentiment_class = "positive" if st.session_state["sentiment"] == "positif" else "negative"
    # Appliquer le style au résultat
    st.markdown(
        f"""
        <div class="result-container {sentiment_class}">
            <span class="result-text">{emoji} {st.session_state["sentiment"].upper()}
            <span class="result-probabitlity">({st.session_state["probabitlity"]:.2%})</span></span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Affichage des boutons seulement si aucun feedback n'a été envoyé
    if not st.session_state["feedback_sent"]:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👍 Correct", key="correct_feedback"):
                st.session_state["feedback"] = "correct"
                st.session_state["feedback_sent"] = True  # Cacher les boutons après clic
                st.rerun()
        with col2:
            if st.button("👎 Incorrect", key="incorrect_feedback"):
                st.session_state["feedback"] = "incorrect"
                st.session_state["feedback_sent"] = True  # Cacher les boutons après clic
                st.rerun()

# Envoi du feedback une fois sélectionné
if st.session_state["feedback"]:
    try:
        response_feedback = requests.post(FEEDBACK_URL, json={
            "text": st.session_state["user_input"],
            "sentiment": st.session_state["sentiment"],
            "probabitlity": st.session_state["probabitlity"],
            "feedback": st.session_state["feedback"]
        })
        if response_feedback.status_code == 200:
            st.success(f"Merci pour votre feedback ({st.session_state['feedback']})")
            # Réinitialiser après envoi
            st.session_state["feedback"] = None
    except requests.exceptions.RequestException as e:
        st.error("Impossible d'envoyer le feedback.")
