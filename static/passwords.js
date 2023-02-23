
/**
 * Fills the table on the page with the
 * received data
 * @param {*} data Array of Ingredient data
 */
let fill_table = (data) =>{
    for(row of data){
        let row_element = form_row([
            row.creator_id, 
            row.creator_name, 
            row.password
        ])
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
get_data()
