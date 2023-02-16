
/**
 * Fills the table on the page with the
 * received data
 * @param {*} data Array of Ingredient data
 */
let fill_table = (data) =>{
    for(row of data){
        let row_element = form_row([
            row.name, 
            row.recipe_count, 
        ])

        // add a link to the end of the end of the row to go to the recipe
        let link_element = document.createElement("a")
        link_element.innerHTML = ("Go to Recipes")
        link_element.href = `/recipes?ingredient=${row.id}`

        let link_column = document.createElement("td")
        link_column.appendChild(link_element)
        row_element.appendChild(link_column)

        // add the row to the table
        let table_body = document.getElementById('table_body')
        table_body.appendChild(row_element)

    }
}

/**
 * Gets recipe data and calls fill_table
 */
let get_data = () =>{
    if (SIMULATE_DATA){
        let simulated_data = [
            {
                "id": 0,
                "name": "Vanilla ice cream",
                "recipe_count": 2,
            },
            {
                "id": 1,
                "name": "Chicken",
                "recipe_count": 3,
            },
            {
                "id": 2,
                "name": "Sriloin Steak",
                "recipe_count": 1,
            },
            {
                "id": 3,
                "name": "Green beans",
                "recipe_count": 1,
            },
            {
                "id": 4,
                "name": "Flour",
                "recipe_count": 7,
            },
        ]
        fill_table(simulated_data)
    }else{
        
        fetch("/ingredients", {
            method: "GET"
        })
        .then(response => response.json())
        .then(response => { 
            fill_table(response)
        })
        
    }
}

/**
 * Performs
 */
let create_ingredient = (name) =>{
    let body = {
        "name": name
    }
    fetch('/ingredients',{
        method: "POST",
        body: JSON.stringify(body),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response =>{
        if(response.status == 200){

            // refresh the page on success
        }else{

            // attempt to get error message from response
            // else use default
            let err_msg = "An error occurred"
            console.log(response)
            if(response.statusText){
                err_msg = response.statusText
            }

            // show error
            document.getElementById("error_message").innerHTML = err_msg
        }
    })
}

// perform data query immediately
get_data()

// allow new ingredient creation on this page
document.getElementById("new_ingredient_btn").addEventListener("click", ()=>{
    
    // validate the ingredient name
    let ingredient_name = document.getElementById("new_ingredient_name").value
    if(ingredient_name.trim().length == 0){
        document.getElementById("error_message").innerHTML = "Cannot submit empty name"
    }else{
        create_ingredient(ingredient_name)
    }
    
})
