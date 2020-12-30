import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    comics = list(mongo.db.books.find())
    return render_template("home.html", comics=comics)


@app.route("/register", methods=["GET", "POST"])
def register():
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
            "password": generate_password_hash(request.form.get("password"))}
        mongo.db.users.insert_one(new_user)
        flash("Registration Complete!")
        return redirect(url_for("home"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            if check_password_hash(
              existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("home", user=session["user"]))
            else:
                return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    flash("You've been logged out.")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/profile/<username>")
def profile(username):
    user = mongo.db.users.find_one({"username": username})
    if session["user"]:
        return render_template("profile.html", user=user)
    return redirect(url_for("login"))


@app.route("/edit_profile/<user_id>", methods=["GET", "POST"])
def edit_profile(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if request.method == "POST":
        change = {
            "first_name": request.form.get("first_name").capitalize(),
            "last_name": request.form.get("last_name").capitalize(),
            "dob": request.form.get("dob"),
            "email": request.form.get("email"),
            "username": session["user"],
            "password": mongo.db.users.find_one(
                {"_id": ObjectId(user_id)})["password"]
        }
        mongo.db.users.update({"_id": ObjectId(user_id)}, change)
        flash("Profile Updated.")
        return redirect(url_for('profile', username=session['user']))

    return render_template("edit_profile.html", user=user)


@app.route("/change_password/<user_id>", methods=["GET", "POST"])
def change_password(user_id):
    if request.method == "POST":
        new_pass = request.form.get("new_password")
        if check_password_hash(mongo.db.users.find_one(
            {"_id": ObjectId(user_id)})["password"],
             request.form.get("old_password")):
            if new_pass == request.form.get("repeat_password"):
                mongo.db.users.update_one({"_id": ObjectId(user_id)},
                                          {"$set": {"password":
                                                    generate_password_hash(
                                                                   new_pass)}})
                flash("Password Changed.")
                return redirect(url_for('profile', username=session['user']))
            else:
                flash("New Password Must Match.")
        else:
            flash("Incorrect Password.")

    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return render_template("change_password.html", user=user)


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)