
/**
 * Fills the table on the page with the
 * received data
 * @param {*} data Array of Recipe data
 */
let fill_table = (data) =>{
    

    for(row of data){
        let row_element = form_row([
            row.id,
            row.name, 
            row.ingredient_count, 
            row.creator, 
            row.date
        ])

        // add a link to the end of the end of the row to go to the recipe
        let link_element = document.createElement("a")
        link_element.innerHTML = ("View Recipe")
        link_element.href = `/recipe/${row.id}`

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
            "name": "Ice cream sundae",
            "creator": "John Snow",
            "ingredient_count": 3,
            "date": "2020-11-08"
        },
        {
            "id": 1,
            "name": "Chicken Fried Rice",
            "creator": "Joyce Bawk",
            "ingredient_count": 6,
            "date": "2015-06-09"
        },
        {
            "id": 2,
            "name": "Grilled Steak",
            "creator": "Terry Moo",
            "ingredient_count": 3,
            "date": "2021-12-07"
        },
        {
            "id": 3,
            "name": "Green bean casserole",
            "creator": "Apple Beanstalk",
            "ingredient_count": 5,
            "date": "2017-07-07"
        },
        {
            "id": 4,
            "name": "Croissant",
            "creator": "Pierre Francais",
            "ingredient_count": 3,
            "date": "2009-03-29"
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


/**
 * 
 * SEARCH INGREDIENTS
 * 
 */

/**
 * 
 * Fills the select menu on the page with the
 * received data
 * @param {*} data Array of Ingredient data
 */
let fill_menu = (data) =>{
    
    // create options dropdown list
    let options = document.createElement("div")
    let values = []

    // first create the empty option
    let option = document.createElement("option")
    option.value = ""
    option.innerHTML = "Select an Ingredient..."
    options.appendChild(option)
    values.push(option.value)

    for(row of data){
        option = document.createElement("option")
        option.value= row.id,
        option.innerHTML = row.name
        
        // build arrays for option elements and values
        options.appendChild(option)
        values.push(option.value)
    }

    // update the dropdown
    let element = document.getElementById("ingredient_select")
    
    // copy the inner html of the template and inject into this one
    element.innerHTML = options.innerHTML
        
}

/**
 * Requests ingredient list from server
 */
let get_ingredient_data = () =>{
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
        .then(response => response.json())
        .then(data => fill_menu(data))
        
        // perform query and then fill table
        
    }
}
get_ingredient_data()

// on click refresh page and search for recipes w/ ingredients
document.getElementById("search_ingredient").addEventListener("click", ()=>{
    let ingredient_id = document.getElementById("ingredient_select").value
    
    let link = document.createElement("a")
    link.href = `/recipes?ingredient=${ingredient_id}`
    link.hidden = true
    document.childNodes[0].appendChild(link)
    link.click()

    
})

/**
 * 
 * SEARCH CREATORS
 * 
 */

/**
 * 
 * Fills the select menu on the page with the
 * received data
 * @param {*} data Array of Ingredient data
 */
let fill_creator_menu = (data) =>{
    
    // create options dropdown list
    let options = document.createElement("div")
    let values = []

    // first create the empty option
    let option = document.createElement("option")
    option.value = ""
    option.innerHTML = "Select a Creator..."
    options.appendChild(option)
    values.push(option.value)

    for(row of data){
        option = document.createElement("option")
        option.value= row.id,
        option.innerHTML = row.name
        
        // build arrays for option elements and values
        options.appendChild(option)
        values.push(option.value)
    }

    // update the dropdown
    let element = document.getElementById("creator_select")
    
    // copy the inner html of the template and inject into this one
    element.innerHTML = options.innerHTML
        
}

/**
 * Requests ingredient list from server
 */
let get_creator_data = () =>{
    if (SIMULATE_DATA){
        let simulated_data = [
            {
                "id": 0,
                "name": "John Snow",
                "recipe_count": 1
            },
            {
                "id": 1,
                "name": "Joyce Bawk",
                "recipe_count": 6,
            },
            {
                "id": 2,
                "name": "Terry Moo",
                "recipe_count": 3,
            },
            {
                "id": 3,
                "name": "Apple Beanstalk",
                "recipe_count": 2,
            },
            {
                "id": 4,
                "name": "Pierre Francais",
                "recipe_count": 3,
            },
        ]
        fill_creator_menu(simulated_data)
    }else{
        
        fetch("/users", {
            method: "GET"
        })
        .then(response =>response.json())
        .then(data => {
            fill_table(data)
        })
        
        // perform query and then fill table
        
    }
}
get_creator_data()

// on click refresh page and search for recipes w/ ingredients
document.getElementById("search_creator").addEventListener("click", ()=>{
    let ingredient_id = document.getElementById("creator_select").value
    
    let link = document.createElement("a")
    link.href = `/recipes?user=${ingredient_id}`
    link.hidden = true
    document.childNodes[0].appendChild(link)
    link.click()

    
})