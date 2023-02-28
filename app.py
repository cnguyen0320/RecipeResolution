from flask import Flask, render_template, redirect, session, url_for, request, abort, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "RecipeResolution"

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_nguyech6'
app.config['MYSQL_PASSWORD'] = '5055' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_nguyech6'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# VIEWS
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recipes')
def recipe_view():
    return render_template('recipes.html')

@app.route("/recipe/<id>", methods=["GET"])
def recipe_single(id):
    # if ID is create, then direct to create recipe page
    if id == "create":
        return render_template("create_recipe.html")
    else:
        creator_id = 0 # TODO get the creator ID who created the recipe
        return render_template("recipe.html", recipe_id=id, creator_id=creator_id)

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
        return render_template("create_recipe.html", recipe=recipe)
    
    # return forbidden
    abort(403)

@app.route("/login", methods=["GET"])
def login_page():
    # if we get to this page with a session, we should pop the session credentials
    session.clear()

    return render_template("login.html")

@app.route("/ingredients", methods=["GET"])
def ingredient_page():
    return render_template("ingredients.html")

@app.route("/creators", methods=["GET"])
def user_page():
    return render_template("creators.html")

@app.route("/passwords", methods =["GET"])
def passwords_page():
    return render_template("passwords.html")

@app.route("/recipe_components", methods =["GET"])
def recipe_components_page():
    return render_template("recipe_components.html", )


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


@app.route("/createUser", methods=["POST"])
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

    # create user and password in DB
    user, user_id = db_createUser(user, password)
    if user_id:
        # auto log in user and return
        session['user'] = user
        session['user_id'] = user_id
        return "ok", 200
    else:
        return "error", 400


@app.route("/logout")
def logout():
    # clear session and return home
    session.clear()
    return redirect(url_for('home'))



@app.route("/ingredient", methods=["GET"])
def getIngredients():
    """
    Gets the ingredients table w/ filter
    """
    result = db_getIngredient({
        "min": request.args.get("min", None),
        "max": request.args.get("max", None)
    })
    print(result)
    return jsonify(result)



@app.route("/ingredient", methods=["POST"])
def createIngredient():
    """
    Creates an Ingredient
    """
    post_data = request.get_json()
    result = db_createIngredient(post_data["name"])

    if result:
        return "ok", 200

    return "An error occurred", 404

@app.route("/ingredient", methods=["DELETE"])
def deleteIngredient():
    """
    Deletes an ingredient
    """
    try:
        db_deleteIngredient(request.args.get("id", None))
    except Exception:
        pass

    return "ok", 200

@app.route("/ingredient", methods=["PUT"])
def updateIngredient():
    """
    Updates an ingredient
    """
    try:
        post_data = request.get_json()
        db_updateIngredient(post_data)
        return "ok", 200

    except Exception:
        return "error", 404


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


"""
Controller code lives below here. Since we are using flask-mysqldb, we will keep the model
and controller in the same file
"""
def db_createIngredient(name):
    # generate the query
    query = "INSERT INTO Ingredients (name) VALUES ('{}');".format(name)

    # execute the query
    cursor = mysql.connection.cursor()
    try:
        cursor.execute(query)
        mysql.connection.commit()
        return True
    except Exception as e:
        return False

def db_getIngredient(filter=None):
    # Generate the filter query
    filter_query = ""
    if filter is not None:
        
        if "min" in filter and filter["min"] is not None:
            filter_query = "HAVING recipeCount >= {}".format(filter["min"])
        else:
            filter_query = "HAVING recipeCount >= 0"
        
        if "max" in filter and filter["max"] is not None:
            filter_query += " AND recipeCount <= {}".format(filter["max"])

    query = """
    SELECT Ingredients.ingredientID AS id, Ingredients.name AS name, COUNT(DISTINCT(RecipeComponents.recipeID)) AS recipeCount
    FROM Ingredients 
    LEFT JOIN RecipeComponents ON Ingredients.ingredientID = RecipeComponents.ingredientID 
    GROUP BY Ingredients.ingredientID
    {}
    ORDER BY Ingredients.name
    ;
    """.format(filter_query)
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    return  cursor.fetchall()

def db_updateIngredient(filter):
    query = "UPDATE Ingredients SET name = '{}' WHERE ingredientId = {}".format(filter["name"], filter["id"])
    print(query)
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    mysql.connection.commit()

def db_deleteIngredient(id):
    query = "DELETE FROM Ingredients WHERE ingredientId = {}".format(id)
    print(query)
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    mysql.connection.commit()
    

def db_createUser(name, password):
    """
    Create new user and password
    """

    try:
        assert(password != "")
        cursor = mysql.connection.cursor()

        # first query insert the user
        query = "INSERT INTO Creators (username) VALUES ('{}')".format(name)
        cursor.execute(query)
        user_row_id = cursor.lastrowid

        print(user_row_id)
        # query insert the password        
        query = "INSERT INTO Passwords (creatorID, password) VALUES ({}, '{}')".format(user_row_id, password)
        cursor.execute(query)

        # commit at the end to save both user and password
        mysql.connection.commit()

        return name, user_row_id
    except Exception as e:
        print(e)
        return None, None


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3457)