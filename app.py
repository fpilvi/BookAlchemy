import os
from flask import Flask, render_template, request, redirect, url_for
from data_models import db, Author, Book

"""
Main Flask application file for the library system.
"""

app = Flask(__name__)

"""
Configure the database URI and initialize the app with SQLAlchemy.
"""
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'library.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

"""
Create tables in the database if they do not already exist.
"""
with app.app_context():
    db.create_all()

from datetime import datetime


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Handles the route for adding a new author to the database.

    If the request method is POST, the author details are collected
    from the form and added to the database. If successful, the user is
    redirected to the homepage.
    """
    if request.method == 'POST':
        name = request.form['name']
        birth_date_str = request.form['birthdate']
        date_of_death_str = request.form['date_of_death']

        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None
        date_of_death = datetime.strptime(date_of_death_str, '%Y-%m-%d').date() if date_of_death_str else None

        author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('home'))  # Redirect to the homepage after successful author addition

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Handles the route for adding a new book to the database.

    Displays a form with available authors if the request method is GET.
    If the method is POST, the book details are collected from the form,
    and the new book is added to the database. A success message is shown
    after the book is added.
    """
    authors = Author.query.all()
    if request.method == 'POST':
        title = request.form['title']
        isbn = request.form['isbn']
        publication_year = request.form['publication_year']
        author_id = request.form['author_id']

        new_book = Book(title=title, isbn=isbn, publication_year=publication_year, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()

        return render_template('add_book.html', message="Book added successfully!", authors=authors)

    return render_template('add_book.html', authors=authors)


@app.route('/')
def home():
    """
    Displays the homepage with a list of all books in the database.
    """
    books = Book.query.all()
    return render_template('home.html', books=books)


@app.route('/sort_books/<sort_by>')
def sort_books(sort_by):
    """
    Sorts the list of books based on the selected criteria (title or author).

    The 'sort_by' parameter determines the sorting order:
    - 'title' will sort by the book title.
    - 'author' will sort by the author's name.
    """
    if sort_by == 'title':
        books = Book.query.order_by(Book.title).all()
    elif sort_by == 'author':
        books = Book.query.join(Author).order_by(Author.name).all()
    else:
        books = Book.query.all()

    return render_template('home.html', books=books)


@app.route('/search_books', methods=['GET'])
def search_books():
    """
    Handles the search functionality for books.

    Searches for books based on the title. If a search query is provided,
    it filters the books based on the query and displays the results.
    """
    search_query = request.args.get('search_query')
    if search_query:
        books = Book.query.filter(Book.title.ilike(f'%{search_query}%')).all()
    else:
        books = []

    return render_template('home.html', books=books)


if __name__ == "__main__":
    app.run(debug=True)