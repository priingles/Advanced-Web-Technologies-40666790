from flask import (Flask,
                   render_template,
                   url_for,
                   session,
                   redirect)

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


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/library")
def library():
    return render_template("library.html")
