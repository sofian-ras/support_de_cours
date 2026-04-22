import streamlit as st
from transformers import pipeline

# Configuration de la page
st.set_page_config(page_title="NLP Suite", page_icon="🤖", layout="wide")
st.title("Suite NLP Multi-Tâches")


###################################################################################
# TODO: Charger les modèles
# summarizer = pipeline("summarization", model="...")
# translator = pipeline("translation", model="...")
# emotion_classifier = pipeline("text-classification", model="...")

@st.cache_resource
def load_models():
    # Résumé
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    # Traduction (Anglais -> Français)
    translator = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")
    
    # Classification d'émotions
    emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
    
    return summarizer, translator, emotion_classifier

# On récupère nos outils
summarizer, translator, emotion_classifier = load_models()

###################################################################################

# TODO: Créer des onglets avec st.tabs()

# Création des 3 onglets
tab1, tab2, tab3 = st.tabs(["📝 Résumé", "🌍 Traduction", "🎭 Émotions"])


# TODO: Onglet 1 : Résumé de texte
#   - Input: st.text_area pour le texte long
#   - Button: "Résumer"
#   - Output: Afficher le résumé

with tab1:
    st.header("Résumé de texte")
    # C'est ici qu'on mettra la logique du résumé
        # On demande le texte à résumer
    texte_long = st.text_area("Entrez votre texte à résumer :", key="summary_input")
    # Bouton pour lancer le résumé
    if st.button("Résumer"):
        if texte_long:
            # On utilise le modèle summarizer
            resultat = summarizer(texte_long, max_length=150, min_length=30, do_sample=False)
            
            # On affiche le résumé
            st.success(resultat[0]['summary_text'])
        else:
            st.warning("Rien à résumer !")

# TODO: Onglet 2 : Traduction
#   - Input: st.text_area pour texte anglais
#   - Button: "Traduire"
#   - Output: Afficher la traduction française

with tab2:
    st.header("Traduction Anglais ➡️ Français")
    
    # On demande le texte en anglais
    anglais = st.text_area("Entrez votre texte en anglais :", key="trad_input")
    
    # Bouton pour lancer la traduction
    if st.button("Traduire"):
        if anglais:
            # On utilise le modèle translator
            resultat = translator(anglais)
            
            # On affiche la traduction
            st.success(resultat[0]['translation_text'])
        else:
            st.warning("Rien à traduire !")

# TODO: Onglet 3 : Classification d'émotions
#   - Input: st.text_input pour une phrase
#   - Button: "Analyser"
#   - Output: Afficher l'émotion détectée

with tab3:
    st.header("Classification d'émotions")
    # C'est ici qu'on mettra la logique de classification d'émotions
    phrase = st.text_input("Entrez une phrase :", key="emotion_input")
    if st.button("Analyser"):
        if phrase:
            # On utilise le modèle emotion_classifier
            resultat = emotion_classifier(phrase)
            
            # On récupère les infos
            label = resultat[0]['label']
            score = resultat[0]['score'] * 100
            
            # On affiche l'émotion détectée avec le score
            st.success(f"Émotion détectée : {label} ({score:.2f}%)")
        else:
            st.warning("Rien à analyser !")