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

# ///////////////////////
#        CREATORS
# SELECT
# UPDATE
# DELETE 
# ///////////////////////

@app.route("/creator", methods=["GET"])
def getCreator():
    '''
    Gets data from table Creators thru db
    '''
    result = db_getCreator()

    if result:
        return jsonify(result)

    return "An error occurred", 404


@app.route("/creators", methods=["PUT"])
def updateCreators():
    """
    Updates Creator username
    """
    try:
        post_data = request.get_json()
        name = post_data['creator_name']
        id = post_data['creator_id']
        db_updateCreator(id, name)
        return "ok", 200

    except Exception:
        return "error", 404
    
@app.route("/creators", methods=["DELETE"])
def deleteCreator():
    """
    Deletes an ingredient
    """
    try:
        db_deleteCreator(request.args.get("id", None))
    except Exception:
        pass

    return "ok", 200
    
# ///////////////////////
#        LOGIN 
#    INSERT for both 
# Creators and Passwords
#      !! WORKS !!
# ///////////////////////

@app.route("/login", methods=["POST"])
def createUser():
    '''
    INSERT for both Creators and Passwords
    Takes input from user at /login page and checks database if username exists.
    If username exists, return error. Else, creates new username & pw.
    Takes no blank fields.
    '''
    # extract credentials
    post_data = request.get_json()
    user = post_data['user']
    password = post_data['password']

    # user exists, do not create new user
    if user_exists(user):
        return "User already exists", 404

    # create user and password in DB
    user, user_id = db_createUser(user, password)
    if user_id:
        # auto log in user and return
        session['user'] = user
        session['user_id'] = user_id
        return "ok", 200
    else:
        return "error", 400

# ///////////////////////
#        PASSWORDS
# SELECT
# UPDATE
# DELETE !! WORKS !!
# ///////////////////////
@app.route("/passwords", methods=["GET"])
def get_userPassword():
    '''
    Gets data from table Passwords
    '''
    result = db_getPassword()
    print(result)
    return jsonify(result)

@app.route("/passwords", methods=["PUT"])
def updatePassword():
    """
    Updates the password of creator in table Passwords
    """
    try:
        post_data = request.get_json()
        password = post_data['password']
        id = post_data['creator_id']
        db_updatePassword(id, password)
        return "ok", 200

    except Exception:
        return "error", 404

@app.route("/passwords", methods=["DELETE"])
def deletePassword():
    """
    Deletes a Password 
    """
    try:
        db_deletePassword(request.args.get("id", None))
    except Exception:
        pass

    return "ok", 200



# ///////////////////////
#      INGREDIENTS
# ///////////////////////
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

# ///////////////////////
#        RECIPES
# INSERT
# UPDATE
# DELETE 
# ///////////////////////

@app.route("/recipe", methods=["GET"])
def getRecipes():
    # generate filter based on query string
    filter = dict()

    filter["creatorID"] = request.args.get("user", None)
    filter["ingredient"] = request.args.get("ingredient", None)

    return jsonify(db_getAllRecipe(filter))
    

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
    
    # perform delete
    db_deleteRecipe(id)
    return "ok", 200
    

"""
Controller code lives below here. Since we are using flask-mysqldb, we will keep the model
and controller in the same file
"""

#####################################################################
# Ingredient
#####################################################################
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
    return cursor.fetchall()

def db_updateIngredient(filter):
    query = "UPDATE Ingredients SET name = '{}' WHERE ingredientId = {}".format(filter["name"], filter["id"])
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    mysql.connection.commit()

def db_deleteIngredient(id):
    query = "DELETE FROM Ingredients WHERE ingredientId = {}".format(id)
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    mysql.connection.commit()

#####################################################################
# User & Password
#####################################################################
def db_getCreator():
    query = "SELECT * FROM Creators"
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    return  cursor.fetchall()

def db_getPassword():
    query = """SELECT Creators.creatorID AS creator_id, Creators.username AS creator_name, Passwords.password AS password 
    FROM Creators 
    INNER JOIN Passwords ON Creators.creatorID = Passwords.creatorID 
    ORDER BY username ASC;
    """
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()

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
    
def user_exists(username):
    """
    Checks if input matches any username on database
    """
    # Connect to the database
    cursor = mysql.connection.cursor()

    # Query the database for the user
    query = ("SELECT * FROM Creators WHERE username = %s")
    cursor.execute(query, (username,))

    # Check if the user exists
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False

def db_updatePassword(id, password):
    """
    Update password on user id
    """
    query = "UPDATE Passwords SET password = '{}' WHERE creatorID = {}".format(password, id)
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    mysql.connection.commit()

def db_deletePassword(id):
    query = "DELETE FROM Passwords WHERE creatorID = {}".format(id)
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    mysql.connection.commit()

def db_updateCreator(id, name):
    """
    Update user to update the username
    """
    query = "UPDATE Creators SET username = '{}' WHERE creatorID = {}".format(name, id)
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    mysql.connection.commit()

def db_deleteCreator(id):
    query = "DELETE FROM Creators WHERE creatorID = {}".format(id)
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    mysql.connection.commit()


#####################################################################
# Recipe TODO
#####################################################################
def db_createRecipe(recipe):
    # TODO
    pass

def db_updateRecipe(recipe):
    # TODO
    pass

def db_getRecipe(id):
    """
    Get a singular recipe based on ID
    """
    # get recipe data
    recipe_query = """
    SELECT Recipes.recipeID AS id, Recipes.description AS description, 
    Recipes.name AS name, Recipes.dateCreated AS date, Creators.username AS creator
    FROM Recipes
    LEFT JOIN Creators ON Recipes.creatorID = Creators.creatorID
    LEFT JOIN RecipeComponents ON Recipes.recipeID = RecipeComponents.recipeID
    WHERE Recipes.recipeID = {}
    ;""".format(id)
    cursor = mysql.connection.cursor()
    cursor.execute(recipe_query)
    recipe_result = cursor.fetchall()[0]

    # get ingredient data
    ingredient_query = """
    SELECT Ingredients.ingredientID AS id, Ingredients.name as name,
    RecipeComponents.quantity as quantity, RecipeComponents.unit as unit, RecipeComponents.required as required
    FROM Ingredients
    RIGHT JOIN RecipeComponents ON Ingredients.ingredientID = RecipeComponents.ingredientID
    WHERE RecipeComponents.recipeID = {}
    """.format(id)
    cursor.execute(ingredient_query)
    ingredient_result = cursor.fetchall()

    # combine the dictionaries
    recipe_result["ingredients"] = ingredient_result

    return recipe_result



def db_getAllRecipe(filter):
    """
    Get all recipes by applying filter
    """
    
    creator_string = ""
    if "creatorID" in filter and filter["creatorID"] is not None:
        creator_string = "Recipe.creatorID = {}".format(filter["creatorID"])

    ingredient_string = ""
    if "ingredient" in filter and filter["ingredient"] is not None:
        ingredient_string = "Ingredients.ingredientID = {}".format(filter["ingredient"])

    filter_string = ""
    if creator_string !="" or ingredient_string != "":
        filter_string = "WHERE " + "AND ".join([creator_string, ingredient_string])

    print(filter)
    
    query = """
    SELECT Recipes.recipeID AS id, Recipes.name AS name, Recipes.dateCreated AS date, Creators.username AS creator, 
    COUNT(DISTINCT RecipeComponents.ingredientID) AS ingredient_count
    FROM Recipes
    LEFT JOIN Creators ON Recipes.creatorID = Creators.creatorID
    LEFT JOIN RecipeComponents ON Recipes.recipeID = RecipeComponents.recipeID
    {}
    GROUP BY Recipes.recipeID
    ;""".format(filter_string)
    print(query)

    cursor = mysql.connection.cursor()
    cursor.execute(query)

    return cursor.fetchall()

def db_deleteRecipe(id):
    query = "DELETE FROM Recipes WHERE recipeID = {}".format(id)
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    mysql.connection.commit()

#####################################################################
# RecipeComponent TODO
#####################################################################
def db_createRecipeComponent():
    # TODO
    pass

def db_getRecipeComponents():
    query = """
    SELECT rc.componentID as id, rc.recipeID as recipe_id, rc.ingredientID as ingredient_id,
    rc.quantity as quantity, rc.unit as unit, rc.required as required
    FROM RecipeComponents rc;
    """

    cursor = mysql.connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def db_updateRecipeComponent():
    # TODO
    pass

def db_deleteRecipeComponent(id):
    query = "DELETE FROM RecipeComponents WHERE componentID = {}".format(id)
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    mysql.connection.commit()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3459)