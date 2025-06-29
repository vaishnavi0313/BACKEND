from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
books = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('Title')
        author = request.form.get('Author')
        content = request.form.get('Content')

        if not title or not author:
            return "Title and Author are required", 400

        new_data = {
            "id": len(books) + 1,
            "title": title,
            "author": author,
            "content": content
        }

        books.append(new_data)
        print(f"Book added: {title} by {author} - {content}")
        return render_template('index.html', message="Book added successfully!")

    return render_template('index.html')
@app.route('/api/books', methods=['GET'])
def get_books():
    return jsonify(books), 200
@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.get_json()
    if not data or 'title' not in data or 'author' not in data:
        return jsonify({'error': 'Title and Author are required'}), 400

    new_data = {
        "id": len(books) + 1,
        "title": data['title'],
        "author": data['author'],
        "content": data.get('content', '')
    }

    books.append(new_data)
    return jsonify(new_data), 201

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    if book:
        return jsonify(book), 200
    return jsonify({'error': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
