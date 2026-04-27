from flask import Flask, request, jsonify
import joblib
from db import init_db, save_prediction

app = Flask(__name__)
model = joblib.load("model.pkl")

init_db()

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json.get('inputs')

    prediction = model.predict([data])
    result = prediction.tolist()[0]

    save_prediction(data, result)

    return jsonify({
        "prediction" : result
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)