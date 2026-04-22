---
title: NLP Multi-Tasks
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.28.0
app_file: app.py
pinned: false
---

# NLP Multi-Tasks Suite

Application Streamlit avec 3 fonctionnalités NLP :

1. Résumé de texte
2. Traduction anglais vers français
3. Classification d'émotions

Version optimisée CPU avec des modèles plus légers.

## Lancer en local

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Modèles utilisés (version légère)

- Résumé : `sshleifer/distilbart-cnn-12-6`
- Traduction : `Helsinki-NLP/opus-mt-en-fr`
- Émotions : `bhadresh-savani/distilbert-base-uncased-emotion`
