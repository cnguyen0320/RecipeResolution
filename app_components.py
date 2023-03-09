
from flask import Flask, render_template, redirect, session, url_for, request, abort, jsonify
from flask_mysqldb import MySQL


app = None   
mysql = None

def config_app(_app, _mysql):
    app = _app
    mysql = _mysql
        
    @app.route("/recipe_components", methods =["GET"])
    def recipe_components_page():
        return render_template("recipe_components.html", )


    # API endpoints

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
