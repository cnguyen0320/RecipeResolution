
/**
 * Fills the table on the page with the
 * received data
 * @param {*} data Array of Recipe data
 */
let fill_table = (data) =>{
    

    for(row of data){
        let row_element = form_row([
            row.name, 
            row.ingredient_count, 
            row.creator, 
            row.date
        ])

        // add a link to the end of the end of the row to go to the recipe
        let link_element = document.createElement("a")
        link_element.innerHTML = ("Go to Recipe")
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

