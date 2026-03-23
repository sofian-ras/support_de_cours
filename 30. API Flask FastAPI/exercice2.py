from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/convert/temp', methods=['GET'])
def convert_temp():
    value = request.args.get('value', type=float)
    unit = request.args.get('unit')

    if value is None or unit is None:
        return jsonify({"error": "Missing 'value' or 'unit' parameter"}), 400

    if unit == 'c2f':
        return jsonify({"celsius": value, "fahrenheit": (value * 9 / 5) + 32})

    if unit == 'f2c':
        return jsonify({"fahrenheit": value, "celsius": (value - 32) * 5 / 9})

    return jsonify({"error": "Use 'c2f' or 'f2c' for unit"}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)