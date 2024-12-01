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
        book = Book(id=data.get("id"), 
                    title=data.get("title"), 
                    author=data.get("author"), 
                    year=data.get("year"),
                    description=data.get("description"),
                    rating=data.get("rating"),
                    image_url=data.get("image_url"))
        # book = Book(**data)
        Config.SESSION.add(book)
        Config.SESSION.commit()
        return jsonify({"success": "Successful operation"})
    except:
        return jsonify({"error": "Enter all values. Title, author, description and image_url (optional) must be string. Year must be integer. Rating (optional) must be float or integer"})


@app.put("/put")
def put():
    data = request.get_json()
    try:
        book = Config.SESSION.get(Book, data.get("id"))
        if not book or type(data.get("id")) != int:
            return jsonify({"error": "Enter the valid id (integer)"})
        Config.SESSION.delete(book)

        newbook = Book(id=data.get("id"),
                  title=data.get("title"), 
                  author=data.get("author"), 
                  year=data.get("year"),
                  description=data.get("description"),
                  rating=data.get("rating", 0),
                  image_url=data.get("image_url", "https://picsum.photos/200/300?blur=5"))
        Config.SESSION.add(newbook)
        Config.SESSION.commit()
        return jsonify({"success": "Successful operation"})
    except:
        return jsonify({"error": "Enter all values. Title, author, description and image_url (optional) must be string. Year must be integer. Rating (optional) must be float or integer"})


@app.patch("/patch")
def patch():
    data = request.get_json()
    try:
        book = Config.SESSION.get(Book, data.get("id"))
        if not book:
            return jsonify({"error": "Enter the valid id (integer)"})
        book.sqlmodel_update(data)
        Config.SESSION.commit()
        return jsonify({"success": "Successful operation"})
    except:
        return jsonify({"error": "Title, author, description and image_url must be string. Year must be integer. Rating must be float or integer"})


@app.delete("/delete")
def delete_book():
    data = request.get_json()
    try:
        book = Config.SESSION.get(Book, data.get("id"))
        Config.SESSION.delete(book)
        Config.SESSION.commit()
        return jsonify({"success": "Successful operation"})
    except:
        return jsonify({"error": "Enter the valid id (integer)"})


if __name__ == "__main__":
    Config.restart_db()
    Config.migrate()
    app.run(debug=True)
