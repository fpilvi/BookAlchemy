from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    """
    Represents an author in the database.

    Attributes:
        id (int): Unique identifier for the author.
        name (str): Name of the author.
        birth_date (date): Birth date of the author.
        date_of_death (date): Date of death of the author, if applicable.
    """
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    def __repr__(self):
        """
        Returns a string representation of the Author object for debugging.

        Returns:
            str: A string in the format "<Author {name}>"
        """
        return f"<Author {self.name}>"

    def __str__(self):
        """
        Returns a string representation of the Author object for display.

        Returns:
            str: The name of the author.
        """
        return self.name


class Book(db.Model):
    """
    Represents a book in the database.

    Attributes:
        id (int): Unique identifier for the book.
        isbn (str): ISBN of the book (13 characters).
        title (str): Title of the book.
        publication_year (int): Year the book was published.
        author_id (int): Foreign key referencing the Author table.
        author (Author): The author of the book (relationship to Author model).
    """
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)

    # Relationship to Author
    author = db.relationship('Author', backref='books', lazy=True)

    def __repr__(self):
        """
        Returns a string representation of the Book object for debugging.

        Returns:
            str: A string in the format "<Book {title}>"
        """
        return f"<Book {self.title}>"

    def __str__(self):
        """
        Returns a string representation of the Book object for display.

        Returns:
            str: The title of the book.
        """
        return self.title