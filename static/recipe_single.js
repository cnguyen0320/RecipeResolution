
const index_start = document.location.pathname.lastIndexOf("/")
const recipe_id = document.location.pathname.substring(index_start+1)

/**
 * Fills the table on the page with the
 * received data
 * @param {*} data Array of Recipe data
 */
let fill_content = (data) =>{
    
    // fill in the easy fields
    document.getElementById("name").innerHTML = data.name
    document.getElementById("date").innerHTML = data.date
    document.getElementById("creator").innerHTML = data.creator
    document.getElementById("description").innerHTML = data.description.replaceAll("\n", "<br>") // replace all new lines with line break


    // fill in ingredients
    for(row of data.ingredients){
        console.log(row)
        let row_element = form_row([
            row.name, 
            `${row.quantity} ${row.unit}`, // concatenate quantity and unit for concise view
        ])

        // add a link to the end of the end of the row to go to the recipes w/ ingredient
        let link_element = document.createElement("a")
        link_element.innerHTML = ("Explore")
        link_element.href = `/recipes?ingredient=${row.id}`

        let link_column = document.createElement("td")
        link_column.appendChild(link_element)
        row_element.appendChild(link_column)

        // add the row to the table
        let table_body = document.getElementById('table_body')
        table_body.appendChild(row_element)

    }
}


if (SIMULATE_DATA){
    let simulated_data = {
        "id": recipe_id,
        "name": "Ice cream sundae",
        "description": "An ice cream sundae is the best type of dessert.\nYou can fill it with whatever you want, but here are my favorites!",
        "creator": "John Snow",
        "creator_id": 0,
        "date": "2020-11-08",
        "ingredients": [
            {id:78, name: "Vanilla Ice Cream", quantity:1, unit:"scoop", required: true},
            {id:74, name: "Chocalate Fudge", quantity:1, unit:"oz", required: false},
            {id:5 ,name: "Graham Crackers", quantity:1, unit:"", required: false},
            {id: 2, name: "Cherry", quantity:1, unit:"", required: false},
        ],
        
    }
    
    fill_content(simulated_data)
}else{
    let query_recipes = () =>{
        fetch("/recipes", {
            method: "GET"
        })
        .then(response =>response.json())
        .then(data =>{
            // if creator id matches the current user

            fill_content(data)
        })
    }
    
    // first thing to do is to query for recipe data
    
}

// set up delete button if it is rendered
try{
    document.getElementById("delete_btn").addEventListener("click", ()=>{
        fetch(`/recipe/${recipe_id}`, {
            method: "DELETE"
        })
        .then(response => {
            window.location = "/recipes"
        })
    })
}catch{}