from flask import Flask, render_template, request, redirect, url_for
from book_model import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"

db.init_app(app)

with app.app_context():
    db.create_all()

all_books = []
@app.route('/')
def home():
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = {
            'title': request.form['bname'],
            'author': request.form['aname'],
            'rating': int(request.form['rating'])
        }
        all_books.append(data)
        return redirect('/')
    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)

