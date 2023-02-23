
/**
 * Fills the table on the page with the
 * received data
 * @param {*} data Array of Recipe data
 */
let fill_table = (data) =>{
    

    for(row of data){
        let row_element = form_row([
            row.id,
            row.recipe_id, 
            row.ingredient_id, 
            row.quantity, 
            row.unit,
            row.required ? "No": "Yes"
        ])
        

        // add a link to the end of the end of the row to go to the recipe
        let link_element = document.createElement("a")
        link_element.innerHTML = ("View Recipe")
        link_element.href = `/recipe/${row.recipe_id}`

        let link_column = document.createElement("td")
        link_column.appendChild(link_element)
        row_element.appendChild(link_column)

        // add the row to the table
        let table_body = document.getElementById('table_body')
        table_body.appendChild(row_element)

    }
}


if (SIMULATE_DATA){
    let simulated_data = [
        {
            "id": 0,
            "recipe_id": 5,
            "ingredient_id": 1,
            "quantity": 3,
            "unit": "pinches",
            "required": true
        },
        {
            "id": 1,
            "recipe_id": 3,
            "ingredient_id": 2,
            "quantity": 2,
            "unit": "oz",
            "required": false
        },{
            "id": 2,
            "recipe_id": 4,
            "ingredient_id": 1,
            "quantity": 1,
            "unit": "",
            "required": true
        },{
            "id": 3,
            "recipe_id": 2,
            "ingredient_id": 2,
            "quantity": 7,
            "unit": "teaspoons",
            "required": false
        },{
            "id": 4,
            "recipe_id": 1,
            "ingredient_id": 1,
            "quantity": 2,
            "unit": "cups",
            "required": false
        },
    ]
    fill_table(simulated_data)
}else{
    let query_recipes = () =>{
        fetch("/recipes", {
            method: "GET"
        })
        .then(response => response.json())
        .then(data =>{
            fill_table(data)
        })
    }
    
    // first thing to do is to query for recipe data
    
}

// add event listener to Create Button
document.getElementById("create_recipe_btn").addEventListener("click", ()=>{

    // if user does not exist, go to login page
    if(false){
        // TODO implement user
        window.location.pathname = "/login"
    }else{
        window.location.pathname = "/recipe/create"
    }

})

