from flask import (
    Flask,
    render_template,
    url_for,
    session,
    redirect,
    request
)
from .books import books

app = Flask(__name__)
app.secret_key = 'key'


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/profile")
def profile():
    session['visited_profile'] = True
    return render_template("profile.html")


@app.route("/profile/stats")
def profile_stats():
    if not session.get('visited_profile'):
        return redirect(url_for('home'))

    records = {
        "courses_completed": 5,
        "projects_done": 3,
        "current_year": 3
    }
    return render_template("profile_stats.html", stats=records)


from flask import request

@app.route("/gallery")
def gallery():
    query = request.args.get("q", "").lower()

    if query:
        filtered_books = [
            b for b in books
            if query in b["title"].lower()
            or query in b["author"].lower()
        ]
    else:
        filtered_books = books

    return render_template(
        "gallery.html",
        books=filtered_books,
        query=query
    )


@app.route("/book/<int:book_id>")
def book_view(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return "Book not found", 404
    return render_template("book_view.html", book=book)


@app.route("/save/<int:book_id>")
def save_book(book_id):
    if "library" not in session:
        session["library"] = []

    if book_id not in session["library"]:
        session["library"].append(book_id)
        session.modified = True

    return redirect(url_for("gallery"))


@app.route("/remove/<int:book_id>")
def remove_book(book_id):
    if "library" in session and book_id in session["library"]:
        session["library"].remove(book_id)
        session.modified = True

    return redirect(url_for("library"))


@app.route("/library")
def library():
    saved_ids = session.get("library", [])
    saved_books = [b for b in books if b["id"] in saved_ids]
    return render_template("library.html", books=saved_books)


@app.route("/about")
def about():
    return render_template("about.html")
