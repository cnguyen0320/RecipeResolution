
/**
 * Fills the table on the page with the
 * received data
 * @param {*} data Array of Recipe data
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
        link_element.href = `/recipes?user=${row.id}`

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
    fill_table(simulated_data)
}else{
    fetch("/users", {
        method: "GET"
    })
    .then(response =>response.json())
    .then(data => {
        fill_table(data)
    })
}

