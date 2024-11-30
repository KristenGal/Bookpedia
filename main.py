from flask import Flask, jsonify, render_template, request
from sqlmodel import select
from config import Config, Book


app = Flask(__name__)


@app.get("/")
def index():
    books = Config.SESSION.scalars(select(Book)).all()
    return render_template("index.html", books=books)

@app.get('/<int:book_id>/')
def book(book_id):
    book = Config.SESSION.get(Book, book_id)
    return render_template('book_info.html', book=book)


@app.post("/add")
def add_book():
    data = request.get_json()

    try:
        book = Book(title=data.get("title"), 
                    author=data.get("author"), 
                    year=data.get("year"),
                    description=data.get("description"),
                    rating=data.get("rating", None),
                    image_url=data.get("image_url", None))
        # book = Book(**data)
        Config.SESSION.add(book)
        Config.SESSION.commit()
        return jsonify({"success": "Successful operation"})
    except:
        return jsonify({"error": "Enter all values. Title, author, description and image_url (optional) must be string. Year must be integer. Rating (optional) must be float or integer"})


@app.put("/")
def put():
    pass

@app.patch("/")
def patch():
    pass

@app.delete("/")
def delete():
    pass


if __name__ == "__main__":
    Config.restart_db()
    Config.migrate()
    app.run(debug=True)
