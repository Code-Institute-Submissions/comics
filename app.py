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
    comics = list(mongo.db.books.find())
    # Only find favourites if session user exists.
    if session.get("user") is not None:
        favourites = list(mongo.db.favourites.find(
            {"username": session["user"]}))
        return render_template("home.html",
                               comics=comics, favourites=favourites)
    else:
        # If no user logged in set mature filter.
        session["mature"] = "yes"
        return render_template("home.html", comics=comics)


###
# Build search function.
# mongodb index set to search
# comic_name, description and author
###
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    comics = list(mongo.db.books.find({"$text": {"$search": query}}))
    if session.get("user") is not None:
        favourites = list(mongo.db.favourites.find(
            {"username": session["user"]}))
    else:
        favourites = []
    return render_template("home.html", comics=comics, favourites=favourites)


@app.route("/favourites", methods=["GET", "POST"])
def favourites():
    # Search favourites of logged in user
    favourites = list(mongo.db.favourites.find(
        {"username": session["user"]}))
    comics = []
    # Iterates through favourites list to fill comics list
    for favourite in favourites:
        comic = list(mongo.db.books.find(
            {"comic_name": {"$eq":
                            favourite["comic_id"]}}))
        comics += comic
    return render_template("home.html", comics=comics, favourites=favourites)


@app.route("/register", methods=["GET", "POST"])
def register():
    ###
    # Gathers new user information
    # and inserts into the users collection.
    # Also checks if there is a user with the
    # username the new user wants.
    ###
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            flash("Username has been taken.")
            # Returns to register page if username exists
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
        # Successfully adds new user.
        mongo.db.users.insert_one(new_user)
        flash("Registration Complete!")
        return redirect(url_for("home"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Checks for existing user.
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            # Checks user age.
            dob = datetime.strptime(existing_user["dob"], "%d/%m/%Y")
            today = date.today()
            age = (today.year - dob.year - ((
                today.month, today.day) < (
                dob.month, dob.day)))
            # Checks database password with user input password.
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                # Sets mature filter if user age is under 16.
                session["mature"] = "yes" if age < 16 else "no"
                if existing_user["mod"] == "yes":
                    # Sets moderator status.
                    session["moderator"] = "yes"
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("home", user=session["user"]))
            else:
                flash("Incorrect Username/Password")
                return redirect(url_for("login"))
        else:
            flash("Incorrect Username/Password")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/logout")
###
# Removes all session cookies
# and sets mature filter to "yes"
##
def logout():
    flash("You've been logged out.")
    session.pop("user")
    if session.get("moderator") is not None:
        session.pop("moderator")
    session["mature"] = "yes"
    return redirect(url_for("login"))


@app.route("/add_favourite", methods=["POST"])
def add_favourite():
    ###
    # Retreives AJAX data as json.
    # Async required to prevent page refreshing
    # on every favourite entry.
    ###
    response = request.get_json()
    comic_id = response["comic_id"]
    # Creates favourite object.
    favourite = {
        "comic_id": comic_id,
        "username": session["user"]
    }
    # Inserts new favourite.
    mongo.db.favourites.insert_one(favourite)
    return jsonify(response)


@app.route("/delete_favourite", methods=["POST"])
def delete_favourite():
    ###
    # Similar to add_favourite function
    # but removes the favourite entry from
    # database instead of insert
    ###
    response = request.get_json()
    comic_id = response["comic_id"]
    unfavourite = {
        "comic_id": comic_id,
        "username": session["user"]
    }
    # Removes favourite.
    mongo.db.favourites.remove(unfavourite)
    return jsonify(response)


@app.route("/profile/<username>")
def profile(username):
    # Fetches users profile information.
    user = mongo.db.users.find_one({"username": username})
    if session["user"]:
        return render_template("profile.html", user=user)
    return redirect(url_for("login"))


@app.route("/edit_profile/<user_id>", methods=["GET", "POST"])
def edit_profile(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if request.method == "POST":
        # Allows editing of user profile.
        change = {
            "first_name": request.form.get("first_name").capitalize(),
            "last_name": request.form.get("last_name").capitalize(),
            "dob": request.form.get("dob"),
            "email": request.form.get("email"),
            "username": session["user"],
            "password": mongo.db.users.find_one(
                {"_id": ObjectId(user_id)})["password"]
        }
        # Updates user's data to reflect changes, if post request.
        mongo.db.users.update({"_id": ObjectId(user_id)}, change)
        flash("Profile Updated.")
        return redirect(url_for('profile', username=session['user']))
    return render_template("edit_profile.html", user=user)


# Allows other moderators to grant moderator status.
@app.route("/moderator/<username>", methods=["POST"])
def moderator(username):
    # Stops moderators from affecting creators mod status.
    if username == "bob134552":
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
        ###
        # Allows user to change password,
        # user must provide old password and new
        # password as well as confirming new
        # password by entering twice to confirm.
        # This is to prevent anyone other than the
        # user from changing their password.
        ###
        new_pass = request.form.get("new_password")
        if check_password_hash(mongo.db.users.find_one(
                {"_id": ObjectId(user_id)})["password"],
                request.form.get("old_password")):
            # Checks new password and repeat password.
            if new_pass == request.form.get("repeat_password"):
                ###
                # If match then hashes new password and
                # sets it as the new password.
                ###
                mongo.db.users.update_one({"_id": ObjectId(user_id)},
                                          {"$set": {"password":
                                                    generate_password_hash(
                                                        new_pass)}})
                flash("Password Changed.")
                return redirect(url_for('profile', username=session['user']))
            else:
                # If new and repeat password don't match.
                flash("New Password Must Match.")
        else:
            # If old password is wrong.
            flash("Incorrect Password.")
    # Fetches user data.
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return render_template("change_password.html", user=user)


@app.route("/new_entry", methods=["POST", "GET"])
def new_entry():
    if request.method == "POST":
        ###
        # Creates new comic entry based on
        # user input. Also sets mature setting to
        # new entry.
        ###
        mature = "yes" if request.form.get("is_mature") else "no"
        new_entry = {
            "comic_name": " ".join(request.form.get(
                "comic_name").title().split()),
            "author": request.form.get("author_name"),
            "genre": request.form.get("genre"),
            "description": request.form.get("comic_description"),
            "buy_from": request.form.get("buy_from"),
            "comic_image": request.form.get("image_link"),
            "brand": request.form.get("brand"),
            "submitted_by": session["user"],
            "is_mature": mature
        }
        # Checks if comic already exists.
        check = list(mongo.db.books.find(
            {"comic_name": new_entry["comic_name"]}))
        ###
        # If the check list is not empty then
        # notifies user that comic already exists.
        ###
        if check != []:
            flash("Comic Already Exists")
            return redirect(url_for('new_entry'))
        # If check is empty then submits the new comic entry.
        mongo.db.books.insert_one(new_entry)
        flash("Successfully Added New Comic!")
        # Returns user to home page.
        return redirect(url_for('home'))
    return render_template("new_entry.html")


@app.route("/edit_entry/<entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    comic = mongo.db.books.find_one({"_id": ObjectId(entry_id)})
    if request.method == "POST":
        ###
        # Allows editing of comic entry if the user
        # is either the original poster or has the
        # moderator status.
        ###
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
            "submitted_by": session["user"],
            "is_mature": mature
        }
        mongo.db.books.update({"_id": ObjectId(entry_id)}, update_entry)
        flash("Comic Updated!")
        return redirect(url_for('home'))
    return render_template("edit_entry.html", comic=comic)


@app.route("/delete_comic/<entry_id>")
def delete_comic(entry_id):
    ###
    # Deletes comic entry, only available to
    # original poster or moderator.
    ###
    mongo.db.books.remove({"_id": ObjectId(entry_id)})
    flash("Comic Deleted")
    return redirect(url_for("home"))


@app.route("/<entry_id>/<comic_name>")
def more_info(entry_id, comic_name):
    # Searches for specified comic data.
    comic = mongo.db.books.find_one({"_id": ObjectId(entry_id)})
    return render_template("comic.html", comic=comic)


# Renders about page.
@app.route("/about")
def about():
    return render_template("about.html")


# Renders contact page.
@app.route("/contact")
def contact():
    return render_template("contact.html")


# If a 404 error then loads 404 page.
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True
    )
