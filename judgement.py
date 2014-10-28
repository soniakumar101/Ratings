from flask import Flask, render_template, redirect, flash, request
import model

app = Flask(__name__)
app.secret_key = "bgntjklhun6jr5hdbc bygtfdrc g6h65vt happy bday sonia"

@app.route("/")
def index():
    user_list = model.session.query(model.User).limit(5).all()
    return render_template("user_list.html", users=user_list)

@app.route("/all_users")
def all_users():
    user_list = model.session.query(model.User).all()
    return render_template("all_users.html", users=user_list)    

@app.route("/new_user")
def addnewuser():
    u = model.User()
    u.email = request.args.get("email")
    u.password = request.args.get("password")
    u.age = request.args.get("age")
    u.zipcode = request.args.get("zipcode")
    model.session.add(u)
    model.session.commit()
    flash("Added new user")
    return render_template("user_list.html")

# @app.route("/<email>")
# def show_movies_rated(email):
#     movies_list = model.session.query()


if __name__ == "__main__":
    app.run(debug = True)