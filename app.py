from flask import Flask, render_template, redirect

app = Flask(__name__)

# VIEWS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recipes')
def recipe_view():
    return render_template('recipes.html')

@app.route("/recipe/<id>", methods=["GET"])
def recipe_single(id):
    if id == "create":
        return render_template("create_recipe.html")
    else:
        return render_template("recipe.html")

@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/ingredients", methods=["GET"])
def ingredient_page():
    return render_template("ingredients.html")

@app.route("/creators", methods=["GET"])
def user_page():
    return render_template("creators.html")



# API endpoints
@app.route("/login", methods=["POST"])
def login():
    # TODO 
    return 200

@app.route("/createuser", methods=["POST"])
def createUser():
    # TODO
    return 200

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
