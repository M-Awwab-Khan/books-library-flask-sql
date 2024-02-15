from flask import Flask, render_template, request, redirect, url_for
from book_model import db, Book

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.title))
        all_books = result.scalars()
        return render_template('index.html', books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = {
            'title': request.form['bname'],
            'author': request.form['aname'],
            'rating': int(request.form['rating'])
        }
        with app.app_context():
            new_book = Book(title=data['title'], author=data['author'], rating=data['rating'])
            db.session.add(new_book)
            db.session.commit()
        return redirect('/')
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    if request.method == 'GET':
        with app.app_context():
            book_to_update = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
            return render_template('edit.html', book=book_to_update)
    else:
        with app.app_context():
            book_to_update = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
            book_to_update.rating = float(request.form['rating'])
            db.session.commit()
            return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    with app.app_context():
        book_to_delete = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
        # or book_to_delete = db.get_or_404(Book, book_id)
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

