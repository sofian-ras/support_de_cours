from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Chargement du modèle
classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

@app.route("/health")
def health():
    return jsonify({
        'status': 'healthy',
        'model' : 'distilbert-base-uncased-finetuned-sst-2-english'
    })

@app.route('/predict', methods=["POST"])
def predict():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "Veuillez saisir un texte"}), 400
    
    # Prédiction
    result = classifier(text)[0]

    return jsonify({
        'text': text,
        'label': result["label"],
        'score': result['score']
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)