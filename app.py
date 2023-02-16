from flask import Flask, render_template, redirect, session, url_for, request

app = Flask(__name__)
app.secret_key = "RecipeResolution"

# VIEWS
@app.route('/')
def home():
    return render_template('index.html', user_id=session["user_id"] if "user_id" in session else None)

@app.route('/recipes')
def recipe_view():
    return render_template('recipes.html', user_id=session["user_id"] if "user_id" in session else None)

@app.route("/recipe/<id>", methods=["GET"])
def recipe_single(id):
    # if ID is create, then direct to create recipe page
    if id == "create":
        return render_template("create_recipe.html", user_id=session["user_id"] if "user_id" in session else None)
    else:
        return render_template("recipe.html", user_id=session["user_id"] if "user_id" in session else None)

@app.route("/login", methods=["GET"])
def login_page():
    # if we get to this page with a session, we should pop the session credentials
    session.clear()

    return render_template("login.html", user_id=session["user_id"] if "user_id" in session else None)

@app.route("/ingredients", methods=["GET"])
def ingredient_page():
    return render_template("ingredients.html", user_id=session["user_id"] if "user_id" in session else None)

@app.route("/creators", methods=["GET"])
def user_page():
    return render_template("creators.html", user_id=session["user_id"] if "user_id" in session else None)



# API endpoints
@app.route("/login", methods=["POST"])
def login():

    post_data = request.get_json()
    user = post_data['user']
    
    # check DB for username and password combination
    # TODO 
    user_valid = True
    user_id = 1

    # user is valid, set the session details 
    if user_valid:
        session['user'] = user
        session['user_id'] = user_id

    # give redirect for home
    return redirect(url_for("home"))


@app.route("/createuser", methods=["POST"])
def createUser():
    
    # extract credentials
    post_data = request.get_json()
    user = post_data['user']
    password = post_data['password']

    # check if user exists yet
    # TODO
    user_exists = False

    # user exists, do not create new user
    if user_exists:
        return 403

    # create user and password in DB
    # TODO

    # auto log in user and return
    session['user'] = user
    session['user_id'] = user_id
    return 200

@app.route("/logout")
def logout():
    # pop the current user and return home
    session.clear()

    return redirect(url_for('home'))

@app.route("/ingredients", methods=["POST"])
def createIngredient():
    # TODO
    return 200

    return "Ingredient already exists", 404

@app.route("/recipe/<id>", methods=["POST"])
def createRecipe(id):
    # TODO
    return 204

@app.route("/recipe/<id>", methods=["PUT"])
def updateRecipe(id):
    # TODO
    return 204

@app.route("/recipe/<id>", methods=["DELETE"])
def deleteRecipe(id):
    # TODO
    return 204

if __name__ == '__main__':
    app.run()
