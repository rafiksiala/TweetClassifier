import streamlit as st
import requests

# API FastAPI tourne en interne sur `127.0.0.1:8000`
API_URL = "http://127.0.0.1:8001/predict/"
FEEDBACK_URL = "http://127.0.0.1:8001/feedback/"

# Custom CSS pour aligner la prédiction et les boutons sur la même ligne
st.markdown(
    """
    <style>
        .result-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background-color: #f9f9f9;
            padding: 12px 15px;
            border-radius: 8px;
            border: 1px solid #ddd;
            width: 50%;
            margin-top: 10px;
        }
        .result-text {
            font-size: 22px;
            font-weight: bold;
            margin: 0;
        }
        .button-container {
            display: flex;
            gap: 8px;
        }
        .feedback-button {
            font-size: 16px;
            padding: 8px 15px;
            border: 2px solid #ccc;
            border-radius: 5px;
            background-color: white;
            color: black;
            cursor: pointer;
            font-weight: bold;
        }
        .feedback-button:hover {
            background-color: #f0f0f0;
        }
        @media (max-width: 600px) {
            .result-container {
                flex-direction: column;
                width: 90%;
            }
            .button-container {
                margin-top: 10px;
                justify-content: center;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Analyse de Sentiment")

# Injecter le CSS pour modifier le bouton
st.markdown(
    """
    <style>
    div.stButton > button {
        font-size: 16px;
        padding: 8px 15px;
        border: 2px solid #ccc;
        border-radius: 5px;
        background-color: white;
        color: black;
        cursor: pointer;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #f0f0f0;
        color: black;
        border: 2px solid #ccc;
    }
    div.stButton > button:active,
    div.stButton > button:focus {
        background-color: #f0f0f0 !important;
        color: black !important;
        outline: none !important; /* Supprime l'effet de focus */
    }
    </style>
    """,
    unsafe_allow_html=True
)

user_input = st.text_area("")

if st.button("Prédire le sentiment"):
    if user_input:
        try:
            response = requests.post(API_URL, json={"name": user_input})
            if response.status_code == 200:
                result = response.json()
                sentiment = result['sentiment']
                confidence = result['confiance']

                emoji = "😊" if sentiment == "positif" else "😠"

                # Affichage de la prédiction avec les boutons à droite
                st.markdown(
                    f"""
                    <div class="result-container">
                        <span class="result-text">{emoji} {sentiment.upper()} <span style="color: #555;">({confidence:.2%})</span></span>
                        <div class="button-container">
                            <form action="" method="post">
                                <button class="feedback-button" name="correct" type="submit">👍</button>
                            </form>
                            <form action="" method="post">
                                <button class="feedback-button" name="incorrect" type="submit">👎</button>
                            </form>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Envoi du feedback
                feedback = None
                if "correct" in st.session_state:
                    feedback = "correct"
                elif "incorrect" in st.session_state:
                    feedback = "incorrect"

                if feedback:
                    requests.post(FEEDBACK_URL, json={
                        "text": user_input,
                        "sentiment": sentiment,
                        "confidence": confidence,
                        "feedback": feedback
                    })

            else:
                st.write(f"Erreur {response.status_code} : {response.text}")
        except requests.exceptions.RequestException as e:
            st.write("Impossible de se connecter à l'API.")
            st.text(str(e))
    else:
        st.warning("Veuillez entrer un texte.")
