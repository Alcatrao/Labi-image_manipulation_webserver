function doLogin() {
    sendCredentials("login");
}
function doRegister() {
    sendCredentials("register");
}




function sendCredentials(login_register) {
    username = document.getElementById("username").value;
    password = document.getElementById("password").value;

    //alert(password)
    if(username == "" || password == "") {
        alert("Por favor insira um nome de utilizador e uma palavra-passe.")
    }
    else {
        acios_doLogin_doRegister(username, password, login_register)    
        
    }


}


function acios_doLogin_doRegister(username, password, login_register) {          //enviar POST ao servidor e receber resposta
	

        var data = new FormData();
        data.append("username", username)
        data.append("password", password)
        
                                
        var xhr = new XMLHttpRequest();
        if (login_register == "login") xhr.open("POST", "/acios/doLogin");
        else xhr.open("POST", "/acios/doRegister");
        


        xhr.onreadystatechange = () => {                                            
            // Call a function when the state changes.
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                // Request finished. Do processing here.
                show_response(JSON.parse( xhr.response ));       
                }
            };

        xhr.send(data);

}


function show_response(response) {
    if (response.result == "html/inicio.html") {
        authenticate(response.userID, "inicio");       
    }
    else {
        alert(response.result);
    }
}



function authenticate(userID, page) {
    if (page == "inicio") {
        window.location = 'http://127.0.0.1:10013/page_'+page+'/?userID='+userID;
    }
    else {
        window.open('http://127.0.0.1:10013/page_'+page+'/?userID='+userID, '_blank');
    }
    
}



function get_page(page) {

        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const userID = urlParams.get('userID')

        authenticate(userID, page)      
              
}



function about() {
    window.open('http://127.0.0.1:10013/page_about', '_blank');
}




function clearInputs() {
    document.getElementById("username").value="";
    document.getElementById("password").value="";
}