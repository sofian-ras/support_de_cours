"""
Flask exercice 1: Hello World multilingue

Usage:
    python exercice1.py
    # server run on http://localhost:5000

    Testing:
    curl http://localhost:5000/hello/english
    curl http://localhost:5000/hello/french
"""

from flask import Flask, request, jsonify

# Créez une application Flask avec une route `/hello/<language>`
# qui retourne "Hello, World!" en anglais si `<language>` est "english" et "Bonjour, le monde!" en français si `<language>` est "french".

app = Flask(__name__)
@app.route('/hello/<language>', methods=['GET'])
def hello(language):
    if language == 'english':
        return "Hello, World!"
    elif language == 'french':
        return "Bonjour, le monde!"
    else:
        return "Language not supported", 400
    
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)