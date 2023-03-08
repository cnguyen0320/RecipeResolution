
/**
 * Fills the table on the page with the
 * received data
 * @param {*} data Array of Ingredient data
 */
let fill_table = (data) =>{

    let table_body = document.getElementById('table_body')
    table_body.innerHTML = ""

    for(row of data){
        let row_element = form_row([
            row.creator_id, 
            row.creator_name, 
            row.password
        ])

        let creator_id = row.creator_id

        //////////////////////////////////////////////////////////////////
        // add a link to the row to update
        //////////////////////////////////////////////////////////////////
        let update_element = document.createElement("button")
        update_element.className = "btn btn-warning"
        update_element.innerHTML = "Update User"
        update_element.addEventListener("click", ()=>{

            let new_name = prompt("Enter new name")

            if (new_name.trim().length > 0){
                fetch(`/passwords`, {
                    method: "PUT",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        "id": creator_id,
                        "name": new_name.trim()
                    })
                })
                .then(response=>{
                    // reload on success
                    if (response.status >= 200 && response.status <300){
                        location.reload()
                    }else{
                        alert("An error occurred")
                    }
                })
            }
            
        })

        let update_column = document.createElement("td")
        update_column.appendChild(update_element)
        row_element.appendChild(update_column)

        //////////////////////////////////////////////////////////////////
        // add a link to the end of the row to delete
        //////////////////////////////////////////////////////////////////
        let delete_element = document.createElement("button")
        delete_element.className = "btn btn-danger"
        delete_element.innerHTML = "Delete"
        delete_element.addEventListener("click", ()=>{
            fetch(`/passwords?id=${creator_id}`, {
                method: "DELETE"
            })
            .then(response=>{
                // reload on success
                if (response.status >= 200 && response.status <300){
                    location.reload()
                }else{
                    alert("An error occurred")
                }
            })
        })

        let delete_column = document.createElement("td")
        delete_column.appendChild(delete_element)
        row_element.appendChild(delete_column)

        table_body.appendChild(row_element)
    }
}

/**
 * Gets password data and calls fill_table
 */
let get_data = () =>{
    if (SIMULATE_DATA){
        let simulated_data = [
            {
                "creator_id": 0,
                "creator_name": "Admin",
                "password": "password",
            },
            {
                "creator_id": 1,
                "creator_name": "EdwardSnowden",
                "password": "hackmeifyoucan",
            },{
                "creator_id": 2,
                "creator_name": "Santa",
                "password": "Iseeyou",
            },{
                "creator_id": 3,
                "creator_name": "jacksparrow",
                "password": "wherestherum",
            },{
                "creator_id": 4,
                "creator_name": "thanos",
                "password": "inevitable",
            },
        ]
        fill_table(simulated_data)
    }else{
        
        fetch("/passwords", {
            method: "GET"
        })
        .then(response => response.json())
        .then(response => { 
            fill_table(response)
        })
        
    }
}


// perform data query immediately
get_data();
