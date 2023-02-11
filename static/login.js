/**
 * Performs login function by POSTing to server
 */
let login = ()=>{
    let user = document.getElementById("user").value
    let password = document.getElementById("password").value
    fetch("/login", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
          },
        body: JSON.stringify({
            user:user,
            password:password
        })
    }).then(response =>{
        
        // error display error
        if(response.status !== 200){
            document.getElementById("error_message").innerHTML = "Invalid credentials or user not found"
        }else{
            window.location = "/"
        }
    })
}

/**
 * Creates a user by POSTing to server
 */
let createUser = ()=>{
    let user = document.getElementById("user").value
    let password = document.getElementById("password").value
    fetch("/createUser", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
          },
        body: JSON.stringify({
            user:user,
            password:password
        })
    }).then(response =>{
        
        // error display error
        if(response.status !== 200){
            document.getElementById("error_message").innerHTML = "Username is taken"
        }else{
            window.location = "/"
        }
    })
}

document.getElementById("login_btn").addEventListener("click", login)