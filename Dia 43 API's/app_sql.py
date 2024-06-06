from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True

# Datos
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

# Conectar a la base de datos y crear tabla
def init_db():
    conn = sqlite3.connect("book.db")
    c = conn.cursor()

    c.execute('''
              CREATE TABLE IF NOT EXISTS books
              (id INTEGER PRIMARY KEY,
              title TEXT,
              author TEXT,
              first_sentence TEXT,
              published TEXT)
              ''')

    c.execute('DELETE FROM books')

    for book in books:
        c.execute('''
                  INSERT INTO books (id, title, author, first_sentence, published)
                  VALUES (?, ?, ?, ?, ?)''',
                  (book['id'], book['title'], book['author'], book['first_sentence'], book['published']))

    conn.commit()
    conn.close()

# Inicializar la base de datos
init_db()

app = Flask(__name__)
app.config["DEBUG"] = True

# Ruta para obtener todos los libros
@app.route('/api/books', methods=['GET'])
def get_books():
    conn = sqlite3.connect("book.db")
    c = conn.cursor()
    c.execute('SELECT * FROM books')
    all_books = c.fetchall()
    conn.close()

    books_list = []
    for book in all_books:
        books_list.append({
            'id': book[0],
            'title': book[1],
            'author': book[2],
            'first_sentence': book[3],
            'published': book[4]
        })

    return jsonify(books_list)

# Ruta para obtener un libro por ID
@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    conn = sqlite3.connect("book.db")
    c = conn.cursor()
    c.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = c.fetchone()
    conn.close()

    if book:
        return jsonify({
            'id': book[0],
            'title': book[1],
            'author': book[2],
            'first_sentence': book[3],
            'published': book[4]
        })
    else:
        return jsonify({'error': 'Libro no encontrado'}), 404

if __name__ == '__main__':
    app.run()
