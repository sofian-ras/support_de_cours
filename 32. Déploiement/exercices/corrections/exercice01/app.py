from flask import Flask, request, jsonify
from transformers import pipeline
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

MODEL_NAME = "papluca/xlm-roberta-base-language-detection"
MAX_LENGTH = 500

detector = pipeline("text-classification", model=MODEL_NAME)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'model': MODEL_NAME})

@app.route('/detect', methods=['POST'])
def detect():
    start = time.time()

    try:
        data = request.json

        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400

        text = data.get('text', '')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        if len(text) > MAX_LENGTH:
            return jsonify({'error': f'Text too long (max {MAX_LENGTH} characters)'}), 400

        result = detector(text)[0]

        inference_time = time.time() - start
        logger.info(f"Detection: {result['label']} ({inference_time:.3f}s)")

        return jsonify({
            'text': text,
            'language': result['label'],
            'confidence': float(result['score']),
            'inference_time': f"{inference_time:.3f}s"
        })

    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/detect/batch', methods=['POST'])
def detect_batch():
    start = time.time()

    try:
        data = request.json
        texts = data.get('texts', [])

        if not texts:
            return jsonify({'error': 'No texts provided'}), 400

        if not isinstance(texts, list):
            return jsonify({'error': 'texts must be a list'}), 400

        # Vérifier la longueur
        for text in texts:
            if len(text) > MAX_LENGTH:
                return jsonify({'error': f'Text too long (max {MAX_LENGTH} characters)'}), 400

        # Prédiction en batch
        results = detector(texts)

        inference_time = time.time() - start
        logger.info(f"Batch detection: {len(texts)} texts ({inference_time:.3f}s)")

        return jsonify({
            'results': [
                {
                    'text': text,
                    'language': res['label'],
                    'confidence': float(res['score'])
                }
                for text, res in zip(texts, results)
            ],
            'count': len(texts),
            'inference_time': f"{inference_time:.3f}s"
        })

    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)