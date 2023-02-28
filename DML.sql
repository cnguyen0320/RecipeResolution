-- Project Title: Recipe Resolution
-- Team Members: Christopher Nguyen, Vi Nguyen
-- Team Number: 30

------------------------------------------------

-- INSERT Operand
-- // Insert new data into Recipes Table//
INSERT INTO Recipes (name, description, creatorID, dateCreated) VALUES
(:recipenameInput, :descriptionInput, :creatoridInput, :dateInput);

-- // Insert new data into RecipeComponents Table//
INSERT INTO RecipeComponents (recipeID, ingredientID, quantity, unit) VALUES
(:recipeidInput, :ingredientidInput, :quantityInput, :unitInput);

-- // Insert new data into Creators Table//
INSERT INTO Creators (username) VALUES
(:usernameInput);

-- // Insert new data into Ingredients Table//
INSERT INTO Ingredients (name) VALUES
(:ingredientInput);

-- // Insert new data into Passwords Table//
INSERT INTO Passwords (creatorID, password) VALUES
(:creatoridInput, :passwordInput);

------------------------------------------------

-- SELECT Operand

-- Display all data from Recipes table
SELECT * FROM Recipes;

-- +----------+-------------------+------------------------------------------------+-----------+-------------+---------+
-- | recipeID | name              | description                                    | creatorID | dateCreated | private |
-- +----------+-------------------+------------------------------------------------+-----------+-------------+---------+
-- |        1 | Lasagna           | Grandma's Italian recipe with mozarella cheese |         1 | 2020-03-19  | NULL    |
-- |        2 | Mac and Cheese    | 3 Cheese mac with chicken                      |         2 | 2022-11-17  | NULL    |
-- |        3 | Meatloaf          | Uncle Jim's Amish Meatloaf                     |         3 | 2017-06-06  | NULL    |
-- |        4 | Soy Sauce Chicken | Sous Vide marinated chicken                    |         4 | 2019-09-25  | NULL    |
-- +----------+-------------------+------------------------------------------------+-----------+-------------+---------+

-- Display name and description of content from Recipes table
SELECT name, description FROM Recipes;

        -- +-------------------+------------------------------------------------+
        -- | name              | description                                    |
        -- +-------------------+------------------------------------------------+
        -- | Lasagna           | Grandma's Italian recipe with mozarella cheese |
        -- | Mac and Cheese    | 3 Cheese mac with chicken                      |
        -- | Meatloaf          | Uncle Jim's Amish Meatloaf                     |
        -- | Soy Sauce Chicken | Sous Vide marinated chicken                    |
        -- +-------------------+------------------------------------------------+

-- Displays username and password of Creators
SELECT Creators.username, Passwords.password FROM Creators
INNER JOIN Passwords ON Creators.creatorID = Passwords.creatorID
ORDER BY username ASC;

        -- +-----------------+-------------------+
        -- | username        | password          |
        -- +-----------------+-------------------+
        -- | JamAndJosh4141  | judgejosh4food456 |
        -- | JohnDoe123      | 123Password       |
        -- | KimOnAWhim789   | Password456       |
        -- | WillCook4Will99 | amishparadise123  |
        -- +-----------------+-------------------+

-- Displays recipe name along with the Username and Data of who created it
SELECT Recipes.name, Creators.username, Recipes.dateCreated FROM Recipes
INNER JOIN Creators ON Recipes.creatorID = Creators.creatorID
ORDER BY name ASC;

        -- +-------------------+-----------------+-------------+
        -- | name              | username        | dateCreated |
        -- +-------------------+-----------------+-------------+
        -- | Lasagna           | JohnDoe123      | 2020-03-19  |
        -- | Mac and Cheese    | KimOnAWhim789   | 2022-11-17  |
        -- | Meatloaf          | WillCook4Will99 | 2017-06-06  |
        -- | Soy Sauce Chicken | JamAndJosh4141  | 2019-09-25  |
        -- +-------------------+-----------------+-------------+

-- Displays name of Recipe with its ingredients and its measurements
SELECT Recipes.name, RecipeComponents.quantity, RecipeComponents.unit, Ingredients.name FROM Recipes
INNER JOIN RecipeComponents ON Recipes.recipeID = RecipeComponents.recipeID
INNER JOIN Ingredients ON RecipeComponents.ingredientID = Ingredients.ingredientID
ORDER BY Recipes.recipeID DESC;

        -- +-------------------+-----------+-------+------------------+
        -- | name              | quantity  | unit  | name             |
        -- +-------------------+-----------+-------+------------------+
        -- | Soy Sauce Chicken |   2.00000 | lbs   | Chicken          |
        -- | Soy Sauce Chicken | 150.00000 | mLs   | Soy Sauce        |
        -- | Meatloaf          | 800.00000 | grams | Ground Beef      |
        -- | Meatloaf          | 250.00000 | grams | Ketchup          |
        -- | Mac and Cheese    |   1.00000 | cup   | Mozarella Cheese |
        -- | Lasagna           | 300.00000 | grams | Tomatos          |
        -- | Lasagna           | 500.00000 | grams | Mozarella Cheese |
        -- +-------------------+-----------+-------+------------------+

------------------------------------------------

-- UPDATE Operand
-- UPDATE name, description, and creatorID of Recipes where it was created on this date
UPDATE Recipes
    SET name = :recipenameInput, description = :descriptionInput, creatorID = :creatoridInput
    WHERE dateCreated = :dateInput;

-- UPDATE name of ingredient where ingredientID = ?
UPDATE Ingredients
    SET name = :ingredientInput
    WHERE ingredientID = :ingredientidInput;

-- Update username of Creator where creatorID = ?
UPDATE Creators
    SET username = :usernameInput
    WHERE creatorID = :creatoridInput;

------------------------------------------------

-- DELETE Operand

-- DELETES whole recipe row which matches the Recipe name
DELETE FROM Recipes WHERE name = :recipenameInput;

-- DELETES recipes created before the date.
DELETE FROM Recipes WHERE dateCreated < :dateInput;

-- DELETES recipes created by Creator 1.
DELETE FROM Recipes WHERE creatorID = :creatoridInput;

-- DELETES Ingredient where name = input
DELETE FROM Ingredients WHERE name = :ingredientInput;

-- DELETES credentials of Creators using creatorID and subquery attached to name of recipe
DELETE FROM Creators WHERE creatorID = (SELECT creatorID FROM Recipes WHERE name = :recipenameInput;);

-- DELETES creator from Creator table
DELETE FROM Creator WHERE creatorID = :creatoridInput;

-- DELETES username from Creator table
DELETE FROM Creator WHERE username = :usernameInput;

------------------------------------------------
