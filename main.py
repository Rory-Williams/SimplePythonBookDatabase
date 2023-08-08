from flask import Flask, render_template, request, \
    redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books-collection.db"
db = SQLAlchemy()  # create db extension
db.init_app(app)  # initialise app

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    print(all_books)
    # for book in all_books:
        # print(book.title)

    return render_template('index.html', books=all_books)


@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == 'POST':
        data = request.form.to_dict()
        if len(data['book']) > 0:
            print(data)
            # all_books.append(request.form.to_dict())
            # print(all_books)
            title = data['book']
            author = data['author']
            rating = float(data['rating'])
            new_book = Book(title=title, author=author, rating=rating)
            # print(new_book.__repr__())
            db.session.add(new_book)
            db.session.commit()
            all_books = db.session.query(Book).all()
            return render_template('index.html', books=all_books)

    return render_template('add.html')


@app.route('/edit', methods=["GET","POST"])
def edit():
    # book_id = request.args['id']
    book_id = request.args.get('id')
    print(book_id)
    book_entry = Book.query.filter_by(id=book_id).first()
    print(book_entry)
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        new_rating = float(data['rating'])
        print(new_rating)
        print(book_entry)
        book_entry.rating = new_rating
        db.session.commit()
        all_books = db.session.query(Book).all()
        print('swapped ratings')
        return render_template('index.html', books=all_books)
    return render_template('edit.html', book_entry=book_entry)

@app.route("/delete")
def delete():
    book_id = request.args.get('id')

    # DELETE A RECORD BY ID
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
    # app.run()

