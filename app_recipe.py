
from flask import Flask, render_template, redirect, session, url_for, request, abort, jsonify
from flask_mysqldb import MySQL


app = None   
mysql = None

def config_app(_app, _mysql):
    app = _app
    mysql = _mysql

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
