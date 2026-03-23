"""
Flask exercice 2: Hello World
Simple Flask app with a single endpoint

Usage:
    python exercice2.py
    # Server runs on http://localhost:5000

Testing:
    curl "http://localhost:5000/convert/temp?value=25&unit=c2f"
    curl "http://localhost:5000/convert/temp?value=77&unit=f2c"
"""

# creer une route '/convert/temp' qui accepte deux parametres query:
# 'value' : la tempereture (nombre)
# 'unit' : "c2f" (celsius to fahrenheit) ou "f2c" (fahrenheit to celsius)

# Exemple:
# ```bash
# curl "http://localhost:5000/convert/temp?value=25&unit=c2f"
# {"celsius": 25, "fahrenheit": 77.0}

# curl "http://localhost:5000/convert/temp?value=77&unit=f2c"
# {"fahrenheit": 77, "celsius": 25.0}

from flask import Flask, request, jsonify


app = Flask(__name__)
@app.route('/convert/temp', methods=['GET'])
def convert_temp():
    value = request.args.get('value')
    unit = request.args.get('unit')
    
    if value is None or unit is None:
        return jsonify({"error": "Missing 'value' or 'unit' parameter"}), 400
    
    try:
        value = float(value)
    except ValueError:
        return jsonify({"error": "'value' must be a number"}), 400
    
    if unit == 'c2f':
        fahrenheit = (value * 9/5) + 32
        return jsonify({"celsius": value, "fahrenheit": fahrenheit})
    elif unit == 'f2c':
        celsius = (value - 32) * 5/9
        return jsonify({"fahrenheit": value, "celsius": celsius})
    else:
        return jsonify({"error": "Invalid 'unit' parameter. Use 'c2f' or 'f2c'."}), 400
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)