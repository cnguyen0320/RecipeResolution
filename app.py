from flask import Flask, render_template, redirect, session, url_for, request, abort

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
        creator_id = 0 # TODO get the creator ID who created the recipe
        return render_template("recipe.html", user_id=session["user_id"] if "user_id" in session else None, recipe_id=id, creator_id=creator_id)

@app.route("/edit/<id>", methods=["GET"])
def recipe_edit(id):
    creator_id = 0 # TODO get the creator ID who created the recipe
    
    # if creator and current user matches, then return the edit page with all the recipe info prefilled
    # TODO this is test data
    recipe = {
        'name': "test",
        'description':"test description\nbooyah",
        'date': "2019-01-01",
        'creator': "John",
        'ingredients':[
            {
                'id': 0,
                'name': "test ingredient",
                'quantity': 5,
                'units': "unit"
            },
            {
                'id': 0,
                'name': "test ingredient2",
                'quantity': 2,
                'units': "units"
            }
        ]
    }
    if True: # TODO uncomment -> # "user_id" in session and creator_id == session["user_id"]:
        return render_template("create_recipe.html", user_id=session["user_id"] if "user_id" in session else None, recipe=recipe)
    
    # return forbidden
    abort(403)

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
    
    # TODO check DB for username and password combination
    user_valid = True
    user_id = 0

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

    # TODO check if user exists yet
    user_exists = False

    # user exists, do not create new user
    if user_exists:
        return 403

    # TODO create user and password in DB

    # auto log in user and return
    session['user'] = user
    session['user_id'] = user_id
    return 200


@app.route("/logout")
def logout():
    # clear session and return home
    session.clear()
    return redirect(url_for('home'))

@app.route("/ingredients", methods=["POST"])
def createIngredient():
    # TODO
    return 200

    return "Ingredient already exists", 404

@app.route("/recipe", methods=["POST"])
def createRecipe():
    # perform abort if POST request was made without being logged in
    if not "user_id" in session:
        abort(403)
    
    # TODO
    return 204

@app.route("/recipe/<id>", methods=["PUT"])
def updateRecipe(id):
    # TODO Get the recipe and check the creator
    creator_id = 0

    if "user_id" in session and creator_id == session["user_id"]:
        #TODO perform delete

        return 204
    
    else:
        abort(403) # forbidden

@app.route("/recipe/<id>", methods=["DELETE"])
def deleteRecipe(id):
    
    # TODO Get the recipe and check the creator
    creator_id = 0
    
    if "user_id" in session and creator_id == session["user_id"]:
        #TODO perform delete

        return "ok"
    else:
        abort(403) # forbidden


if __name__ == '__main__':
    app.run()
