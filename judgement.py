from flask import Flask, render_template, redirect, flash, request, session
import model

app = Flask(__name__)
app.secret_key = "bgntjklhun6jr5hdbc bygtfdrc g6h65vt happy bday sonia"
modelsession = model.session

@app.route("/")
def index():
    user_list = modelsession.query(model.User).limit(5).all()
    return render_template("user_list.html", users=user_list)

@app.route("/all_users")
def all_users():
    user_list = modelsession.query(model.User).all()
    return render_template("all_users.html", users=user_list)    

@app.route("/new_user")
def addnewuser():
    u = model.User()
    u.email = request.args.get("email")
    u.password = request.args.get("password")
    u.age = request.args.get("age")
    u.zipcode = request.args.get("zipcode")
    modelsession.add(u)
    modelsession.commit()
    flash("Added new user")
    return render_template("user_list.html")

@app.route("/users/<userid>")
def show_movies_rated(userid):
    user = modelsession.query(model.User).get(userid)
    ratings = modelsession.query(model.Rating).filter_by(user_id=user.id).all()
    moviesandratings = {}
    for r in ratings:
        movie = modelsession.query(model.Movie).get(r.movie_id)
        movie = movie.name
        moviesandratings[movie] = r.rating
    keys = moviesandratings.keys()
    return render_template("ratingsinfo.html", info=moviesandratings, keys = keys) 

@app.route("/login", methods=["GET"])
def show_login():
    if "user_id" in session:
        del session["user_id"]
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    print email
    # password = request.form.get("password")

    user = modelsession.query(model.User).filter_by(email = email).first()
    print user

    if user:
         session["user_id"] = user.id
         flash("Successfully logged in")
         return redirect ("/")
    else:
         flash("Username not found")
         return redirect("/login")    

@app.route("/movie/<int:id>", methods=['GET'])
def view_movie(id):
    movie = modelsession.query(model.Movie).get(id)
    ratings = movie.ratings
    rating_nums = []
    user_rating = None
    for r in ratings:
        if r.user_id == session['user_id']:
            user_rating = r
        rating_nums.append(r.rating)
        avg_rating = float(sum(rating_nums))/len(rating_nums)

        #Prediction code: only predict if the user hasn't rated it.
        user = modelsession.query(model.User).get(session['user_id'])
        prediction = None
        if not user_rating:
            prediction = user.predict_rating(movie)
            effective_rating = prediction
        else:
            effective_rating = user_rating.rating
        the_eye = modelsession.query(model.User).filter_by(email="theeye@ofjudgement.com").one()
        eye_rating = modelsession.query(model.Rating).filter_by(user_id=the_eye.id,
        movie_id=movie.id).first()

        if not eye_rating:
            eye_rating = the_eye.predict_rating(movie)
        else:
            eye_rating = eye_rating.rating

        difference = abs(eye_rating - effective_rating)

        messages = [ "I suppose you don't have such bad tast after all.",
                     "I regret every decision that I've ever made that has brought me to listen to your opinion",
                     "Words fail me, as your taste in movies has clarly failed you.",
                     "That movie is great.  For a clown to watch.  Idiot."
                     ]

        beratement = messages[int(difference)]
        #End prediction

        return render_template("movie.html", movie=movie,
                average=avg_rating, user_rating=user_rating,
                prediction=prediction, beratement = beratement)



if __name__ == "__main__":
    app.run(debug = True)