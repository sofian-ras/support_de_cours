from flask import Flask, request, jsonify

app = Flask(__name__)

books = []


@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books), 200


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    for book in books:
        if book['id'] == book_id:
            return jsonify(book), 200

    return jsonify({"error": "Book not found"}), 404


@app.route('/books', methods=['POST'])
def add_book():
    # Lit le JSON envoyé dans la requête
    data = request.get_json()

    if not data or 'title' not in data or 'author' not in data or 'year' not in data:
        return jsonify({"error": "Missing title, author, or year"}), 400

    book_id = len(books) + 1

    new_book = {
        "id": book_id,
        "title": data['title'],
        "author": data['author'],
        "year": data['year']
    }

    books.append(new_book)

    return jsonify(new_book), 201


if __name__ == '__main__':
    app.run(debug=True, port=5000)