from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модель Книги (7 полей)
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(20), unique=True)
    year_published = db.Column(db.Integer)
    price = db.Column(db.Float, default=0.0)
    available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Модель Читателя (7 полей)
class Reader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    birth_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    registration_date = db.Column(db.Date, default=datetime.now().date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Список книг
@app.route('/books')
def books():
    all_books = Book.query.all()
    return render_template('books.html', books=all_books)

# Добавить книгу
@app.route('/books/create', methods=['GET', 'POST'])
def create_book():
    if request.method == 'POST':
        book = Book(
            title=request.form['title'],
            author=request.form['author'],
            isbn=request.form['isbn'],
            year_published=request.form['year_published'],
            price=request.form['price'],
            available=True if 'available' in request.form else False
        )
        db.session.add(book)
        db.session.commit()
        flash('Книга добавлена!', 'success')
        return redirect(url_for('books'))
    return render_template('create_book.html')

# Список читателей
@app.route('/readers')
def readers():
    all_readers = Reader.query.all()
    return render_template('readers.html', readers=all_readers)

# Добавить читателя
@app.route('/readers/create', methods=['GET', 'POST'])
def create_reader():
    if request.method == 'POST':
        reader = Reader(
            full_name=request.form['full_name'],
            email=request.form['email'],
            phone=request.form['phone'],
            birth_date=request.form['birth_date'],
            is_active=True if 'is_active' in request.form else False,
            registration_date=request.form['registration_date']
        )
        db.session.add(reader)
        db.session.commit()
        flash('Читатель добавлен!', 'success')
        return redirect(url_for('readers'))
    return render_template('create_reader.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
