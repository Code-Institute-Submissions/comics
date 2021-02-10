import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, jsonify)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
# allows for use of break and continue in jinja template.
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    '''
    This method renders the home page of the site.
    All comics in the database are displayed and favourites are
    shown if there is a user logged in.
    This method also enables the search bar to return a users query.
    '''
    query = request.args.get("query")
    if query is not None:
        comics = list(mongo.db.books.find({"$text": {"$search": query}}))
    else:
        comics = list(mongo.db.books.find().sort("_id", -1).limit(12))
    if session.get("username") is not None:
        favourites = list(mongo.db.favourites.find(
            {"username": session["username"]}))
        return render_template("home.html",
                               comics=comics, favourites=favourites, title="Home")
    else:
        # If no username logged in set mature filter.
        session["mature"] = "yes"
        return render_template("home.html", comics=comics, title="Home")


@app.route("/favourites", methods=["GET", "POST"])
def favourites():
    '''
    This method gathers all of the user's favourited
    comics and displays them.
    '''
    if session.get("username") is not None:    
        favourites = list(mongo.db.favourites.find(
            {"username": session["username"]}))
        comics = []
        for favourite in favourites:
            comic = list(mongo.db.books.find(
                {"comic_name": {"$eq":
                                favourite["comic_name"]}}))
            comics += comic
        return render_template("home.html", comics=comics, favourites=favourites, title="My Favourites")
    else:
        flash("Please Register/Log in first.")
        return redirect(url_for("home"))


@app.route("/my_submissions", methods=["GET", "POST"])
def my_submissions():
    # This method displays all of the user submissions.
    if session.get("username") is not None:    
        comics = list(mongo.db.books.find({"submitted_by": session["username"]}))
        favourites = list(mongo.db.favourites.find(
            {"username": session["username"]}))
        return render_template("home.html", comics=comics,
        favourites=favourites, title="My Submissions")
    else:
        flash("Please Register/Log in first.")
        return redirect(url_for("home"))


@app.route("/register", methods=["GET", "POST"])
def register():
    '''
    Gathers new user information
    and inserts into the users collection.
    Also checks if there is a user with the
    username the new user wants.
    '''
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            flash("Username has been taken.")
            return redirect(url_for("register"))
        new_user = {
            "first_name": request.form.get("first_name").capitalize(),
            "last_name": request.form.get("last_name").capitalize(),
            "dob": request.form.get("dob"),
            "email": request.form.get("email"),
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "mod": "no"
        }
        mongo.db.users.insert_one(new_user)
        flash("Registration Complete!")
        return redirect(url_for("home"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    '''
    This method allows the user to login,
    Checks data supplied by user with data on the
    users collection to ensure a match and allow 
    user to log in.
    If incorrect log in user is notified.
    '''
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            # Checks user age.
            dob = datetime.strptime(existing_user["dob"], "%d/%m/%Y")
            today = date.today()
            age = (today.year - dob.year - ((
                today.month, today.day) < (
                dob.month, dob.day)))
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["username"] = request.form.get("username").lower()
                # Sets mature filter if user age is under 16.
                session["mature"] = "yes" if age < 16 else "no"
                if existing_user["mod"] == "yes":
                    # Sets moderator status.
                    session["moderator"] = "yes"
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("home", user=session["username"]))
            else:
                flash("Incorrect Username/Password")
                return redirect(url_for("login"))
        else:
            flash("Incorrect Username/Password")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    '''
    This method clears the users session cookie
    and sets the mature filter on.
    Returns user to log in page.
    '''
    flash("You've been logged out.")
    session.pop("username")
    if session.get("moderator") is not None:
        session.pop("moderator")
    session["mature"] = "yes"
    return redirect(url_for("login"))


@app.route("/add_favourite", methods=["POST"])
def add_favourite():
    '''
    Retreives AJAX data as json.
    Async required to prevent page refreshing
    on every favourite entry.
    '''
    response = request.get_json()
    comic_name = response["comic_name"]
    # Creates favourite object.
    favourite = {
        "comic_name": comic_name,
        "username": session["username"]
    }
    mongo.db.favourites.insert_one(favourite)
    return jsonify(response)


@app.route("/delete_favourite", methods=["POST"])
def delete_favourite():
    '''
    Similar to add_favourite function
    but removes the favourite entry from
    database instead of insert
    '''
    response = request.get_json()
    comic_name = response["comic_name"]
    unfavourite = {
        "comic_name": comic_name,
        "username": session["username"]
    }
    mongo.db.favourites.remove(unfavourite)
    return jsonify(response)


@app.route("/profile/<username>")
def profile(username):
    # Fetches users profile information.
    user = mongo.db.users.find_one({"username": username})
    if user is None:
        flash("Username: '{}' doesn't exist.".format(username))
        return redirect(url_for("home"))
    return render_template("profile.html", user=user)


@app.route("/edit_profile/<user_id>", methods=["GET", "POST"])
def edit_profile(user_id):
    '''
    This method allows users to modify their profile
    information from the data stored on the user database.
    It returns the user to their profile page after submitting
    a new change.
    '''
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if request.method == "POST":
        change = {
            "first_name": request.form.get("first_name").capitalize(),
            "last_name": request.form.get("last_name").capitalize(),
            "dob": request.form.get("dob"),
            "email": request.form.get("email"),
            "username": session["username"]
        }
        # Updates user's data to reflect changes, if post request.
        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set":change})
        flash("Profile Updated.")
        return redirect(url_for('profile', username=session['username']))
    return render_template("edit_profile.html", user=user)


@app.route("/moderator/<username>", methods=["POST"])
def moderator(username):
    '''
    This method allows moderators to give and take
    moderator status from other users.
    '''
    if username == "bob134552":
        # Stops moderators from affecting creators mod status.
        flash("Cannot change creators status.")
        return redirect(url_for('profile', username=username))
    else:
        mod = "yes" if request.form.get("is_mod") else "no"
        mongo.db.users.update_one({"username": username}, {
                                  "$set": {"mod": mod}})
        if mod == "yes":
            flash("{} is now a moderator.".format(username))
        else:
            flash("{} is no longer a moderator.".format(username))
        return redirect(url_for('profile', username=username))


@app.route("/change_password/<user_id>", methods=["GET", "POST"])
def change_password(user_id):
    if request.method == "POST":
        '''
        Allows user to change password,
        user must provide old password and new
        password as well as confirming new
        password by entering twice to confirm.
        This is to prevent anyone other than the
        user from changing their password.
        '''
        new_pass = request.form.get("new_password")
        if check_password_hash(mongo.db.users.find_one(
                {"_id": ObjectId(user_id)})["password"],
                request.form.get("old_password")):
            # Checks new password and repeat password.
            if new_pass == request.form.get("repeat_password"):
                mongo.db.users.update_one({"_id": ObjectId(user_id)},
                                          {"$set": {"password":
                                                    generate_password_hash(
                                                        new_pass)}})
                flash("Password Changed.")
                return redirect(url_for('profile', username=session['username']))
            else:
                # If new and repeat password don't match.
                flash("New Password Must Match.")
        else:
            flash("Incorrect Password.")
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return render_template("change_password.html", user=user)


@app.route("/new_comic", methods=["POST", "GET"])
def new_comic():
    '''
    Creates new comic entry based on
    user input. Also sets mature setting to
    new entry.
    '''
    if session.get("username") is not None:
        if request.method == "POST":
            mature = "yes" if request.form.get("is_mature") else "no"
            new_comic = {
                "comic_name": " ".join(request.form.get(
                    "comic_name").title().split()),
                "author": request.form.get("author_name"),
                "genre": request.form.get("genre"),
                "description": request.form.get("comic_description"),
                "buy_from": request.form.get("buy_from"),
                "comic_image": request.form.get("image_link"),
                "brand": request.form.get("brand"),
                "submitted_by": session["username"],
                "is_mature": mature
            }
            check = list(mongo.db.books.find(
                {"comic_name": new_comic["comic_name"]}))
            '''
            If the check list is not empty then
            notifies user that comic already exists.
            '''
            if check != []:
                flash("Comic Already Exists")
                return redirect(url_for('new_comic'))
            # If check is empty then submits the new comic entry.
            mongo.db.books.insert_one(new_comic)
            flash("Successfully Added New Comic!")
            return redirect(url_for('home'))
        return render_template("new_comic.html")
    else:
        reirect(url_for("home"))


@app.route("/edit_entry/<entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    comic = mongo.db.books.find_one({"_id": ObjectId(entry_id)})
    if request.method == "POST":
        '''
        Allows editing of comic entry if the user
        is either the original poster or has the
        moderator status.
        '''
        mature = "yes" if request.form.get("is_mature") else "no"
        update_entry = {
            "comic_name": " ".join(request.form.get(
                "comic_name").title().split()),
            "author": request.form.get("author_name"),
            "genre": request.form.get("genre"),
            "description": request.form.get("comic_description"),
            "buy_from": request.form.get("buy_from"),
            "comic_image": request.form.get("image_link"),
            "brand": request.form.get("brand"),
            "is_mature": mature
        }
        mongo.db.books.update({"_id": ObjectId(entry_id)}, {"$set": update_entry})
        flash("Comic Updated!")
        return redirect(url_for('home'))
    return render_template("edit_entry.html", comic=comic)


@app.route("/delete_comic/<entry_id>")
def delete_comic(entry_id):
    '''
    Deletes comic entry, only available to
    original poster or moderator.
    '''
    mongo.db.books.remove({"_id": ObjectId(entry_id)})
    flash("Comic Deleted")
    return redirect(url_for("home"))


@app.route("/<comic_name>/<entry_id>")
def more_info(entry_id, comic_name):
    # This method returns the selected comics page.
    comic = mongo.db.books.find_one({"_id": ObjectId(entry_id)})
    return render_template("comic.html", comic=comic)


@app.route("/contact")
def contact():
    # This method returns the contact page.
    return render_template("contact.html")


@app.errorhandler(404)
def page_not_found(e):
    # This method handles 404 errors and returns the 404 page.
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True
    )
