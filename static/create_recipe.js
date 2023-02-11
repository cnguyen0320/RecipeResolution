
/**
 * Fills the select menu on the page with the
 * received data
 * @param {*} data Array of Ingredient data
 */
let fill_menu = (data) =>{
    
    // create options dropdown list
    let options = document.createElement("div")
    let values = []
    for(row of data){
        let option = document.createElement("option")
        option.value= row.id,
        option.innerHTML = row.name
        
        // build arrays for option elements and values
        options.appendChild(option)
        values.push(option.value)
    }

    // update the template
    let template_node = document.getElementById("hidden_ingredient_template").getElementsByClassName("ingredient_select")[0]
    
    template_node.innerHTML = options.innerHTML
    console.log(template_node)

    let select_elements = document.getElementsByClassName("ingredient_select")
    for(element in select_elements){
        // capture the current value to not overwrite
        let old_value = element.value
        
        // copy the inner html of the template and inject into this one
        element.innerHTML = template_node.innerHTML

        // restore the old value
        if(old_value in values){
            element.value = old_value
        }else{
            element.value = "" // clear value if ingredient disappears
        }
        
    }
    
}

/**
 * Requests ingredient list from server
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
        fill_menu(simulated_data)
    }else{
        
        fetch("/ingredients", {
            method: "GET"
        })
        
        // perform query and then fill table
        
    }
}

let add_ingredient_row = ()=>{
    let template_node = document.getElementById("hidden_ingredient_template")

    // create new node and remove the hidden attribute
    let new_node = template_node.cloneNode(true)
    new_node.hidden = false
    new_node.value = ""
    new_node.id = "" //clear ID

    document.getElementById("table_body").appendChild(new_node)

}

// perform ingredient data query immediately
get_data()

// start with a single ingredient row
add_ingredient_row()


/**
 * Adds another row to the table on click
 */
document.getElementById("add_ingredient").addEventListener("click", add_ingredient_row)

// refresh input list on button press
document.getElementById("refresh_ingredients").addEventListener("click", get_data)
