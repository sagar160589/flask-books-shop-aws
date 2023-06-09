import os

from flask import Flask, render_template, request, redirect, url_for, flash

from models import Book, db

app = Flask(__name__)

with app.app_context():
    rds_endpoint = os.environ.get('RDS_ENDPOINT')
    app.config['SQLALCHEMY_DATABASE_URI'] = rds_endpoint
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskaws.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = "somethingunique"
    db.init_app(app)
    db.create_all()




@app.route('/')
def index():
    books = Book.query.all()
    print(os.environ.get('PYTHONPATH'))
    return render_template('index.html', books=books)

@app.route('/add/', methods =['POST'])
def insert_book():
    if request.method == "POST":
        book = Book(
            title = request.form.get('title'),
            author = request.form.get('author'),
            price = request.form.get('price')
        )
        db.session.add(book)
        db.session.commit()
        flash("Book added successfully")
        return redirect(url_for('index'))


@app.route('/update/', methods = ['POST'])
def update():
    if request.method == "POST":
        my_data = Book.query.get(request.form.get('id'))

        my_data.title = request.form['title']
        my_data.author = request.form['author']
        my_data.price = request.form['price']

        db.session.commit()
        flash("Book is updated")
        return redirect(url_for('index'))

@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Book.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Book is deleted")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)