from flask import  \
        (Flask, 
        render_template, 
        jsonify, 
        request,
        session,
        redirect,
        url_for)
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import pathlib
from random import randint
import datetime

basedir = pathlib.Path(__file__).parent.resolve()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{basedir/'library.db'}"

app.secret_key = b"\xdb\xfe\xbf'\xa3\x9f\xd1\x16Ou\x16;\xfc\x10CY"

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)

    def obj_to_dict(self):
        return {
            "user_id": self.id,
            "username": self.username,
            "password": self.password
        }

class Authors(db.Model):
    author_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def obj_to_dict(self):
        return {"author_id": self.author_id, "author_name": self.name}
        
class Books(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    bookname = db.Column(db.String(50), nullable=False)
    publisher = db.Column(db.String(50))
    rating = db.Column(db.Float)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)

    def obj_to_dict(self):
        return {
            "book_id": self.book_id,
            "bookname": self.bookname,
            "publisher": self.publisher,
            "author_id": self.author_id,
            "rating": self.rating
        }
class Feedback(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.String(400), nullable=False)
    rating = db.Column(db.Float)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    def obj_to_dict(self):
        return {
            "review_id": self.review_id,
            "review": self.review,
            "rating": self.rating,
            "book_id": self.book_id,
            "user_id": self.user_id
        }


class Loans(db.Model):
    loan_id = db.Column(db.Integer, primary_key=True)
    borrowed_date = db.Column(db.DateTime)
    returned = db.Column(db.Boolean)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def obj_to_dict(self):
        return {
            "loan_id": self.loan_id,
            "borrowed_date": self.borrowed_date,
            "returned": self.returned,
            "book_id": self.book_id,
            "user_id": self.user_id
        }


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided in the requested body"}), 400
    
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "No data provided in the requested body"}), 400

    user = Users.query.filter(
        Users.password == password
    ).filter(
        Users.username == username
    ).first()

    if not user:
        return jsonify({'error': 'Invalid username or password.'}), 401
    
    session["user_id"] = user.id

    return jsonify({
        'user_id': user.id,
        'username': user.username
    }), 200
    

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided in the request body.'}), 400
    
    new_feedback = Feedback(review_id=randint(1,100),\
         review=data.get('feedback'), rating=4.0, book_id=1, user_id=2)
    db.session.add(new_feedback)
    db.session.commit()

    return jsonify({'message': 'Feedback added successfully.'}), 201

@app.route("/user/<string:username>")
def users(username):
    user = Users.query.filter(
        Users.username.like(f"%{username}%")).first()
    return jsonify(user.obj_to_dict())

@app.route("/book/<int:book_id>")
def book(book_id):
    books = Books.query.filter_by(book_id=book_id).all()
    result = [book.obj_to_dict() for book in books]
    return jsonify(result)

@app.route("/loans/<int:book_id>")
def loans(book_id):
    loans = Loans.query.filter_by(book_id=book_id).all()
    result = [loan.obj_to_dict() for loan in loans]
    return jsonify(result)

@app.route("/borrow/", methods=["POST"])
def borrow():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided in the request body.'}), 400

    loan_id = randint(1, 10000)
    new_borrow=Loans(loan_id=loan_id,\
        borrowed_date=datetime.datetime.now(),
        returned=False,
        book_id=data.get('book_id'),
        user_id=data.get('user_id'))
    db.session.add(new_borrow)
    db.session.commit()

    return jsonify({'message': 'Loan added successfully.', 'loan_id': loan_id}), 201

@app.route("/return_book/", methods=["POST"])
def return_book():
    data = request.get_json()

    loan_id = data.get("loan_id")

    if not data:
        return jsonify({'error': 'No data provided in the request body.'}), 400
    
    loan = Loans.query.filter_by(
        loan_id=loan_id
    ).first()

    if not loan.returned:
        loan.returned = True
        db.session.commit()
        return jsonify({'message': 'Book returned successfully.'}), 201
    else:
        return jsonify({'message': 'Book already returned'}), 301


@app.route("/search/<string:bookname>")
def search(bookname):
    books = Books.query.filter(
        Books.bookname.like(f"%{bookname}%")
    ).all()
    result = [book.obj_to_dict() for book in books]
    return jsonify(result)

@app.route("/author/<int:author_id>")
def author(author_id):
    authors = Authors.query.filter_by(author_id=author_id).all()
    result = [author.obj_to_dict() for author in authors]
    return jsonify(result)


