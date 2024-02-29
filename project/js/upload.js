// Image UpLoad Javascript
var file;

function updatePhoto(event) {
	var reader = new FileReader();
	reader.onload = function(event) {
		//Create an imagem
		var img = new Image();
		img.onload = function() {
			//Put imagen on screen
			const canvas = $("#photo")[0];
			const ctx = canvas.getContext("2d");
			ctx.drawImage(img,0,0,img.width,img.height,0,0,550, 450);
		}
		img.src = event.target.result;
	}

	file = event.target.files[0];
	//Obtain the file
	reader.readAsDataURL(file);
}

function uploadImage() {
    if(file != null) {
        sendFile(file);
        //Release the resources alocated to the selected image
        window.URL.revokeObjectURL(picURL);    
    }
    else alert("Imagem em falta!");
}

function sendFile(file) {
	var data = new FormData();
	data.append("myFile", file);


	//Obtain nameImg and authorImg and fill the form
	var name = document.getElementById("nameImg").value;		//meter na variável "name" o texto escrito no input da página upload.html (que invoca esta página .js no seu cabeçalho) com id="nameImg"
	var author = document.getElementById("authorImg").value;	//mesma coisa que acima, mas para o elemento com id="authorImg"


	data.append("nameImg", name)								//o que é enviado é um ficheiro XML, com chaves e valores; na linha 34, é criada a chave "myFile", que é usada na app.py, e que contém todos os dados da imagem
	data.append("authorImg", author)							//agora mete-se os nomes da imagem e do autor em chaves diferentes, e é tudo enviado de uma só vez. Para aceder a cada valor na app.py, basta usar o nome da chave
																//aparentemente, só é possível aceder a estes valores na app.py se a função que os lê (neste caso, upload) tiver como parâmetros os nomes das chaves, caso contrário, essas chaves e esses valores não são lidos
	if (name == "" || author == "") alert("Missing comment and/or username!");
	else {
		var xhr = new XMLHttpRequest();
		xhr.open("POST", "/upload");
		xhr.upload.addEventListener("progress", updateProgress(this), false);
		xhr.send(data);
	}
}

function updateProgress(evt){
	if(evt.loaded == evt.total) alert("Submitted successfully.");
}



function autofill() {
	//dar autofill e readonly ao input do autor, com o nome com que o utlizador fez o login
	const queryString = window.location.search;
	const urlParams = new URLSearchParams(queryString);
	const userID = urlParams.get('userID');
	var resposta;

	var data = new FormData();
    data.append("userID", userID)
   
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/getUsername");
	xhr.send(data);

	xhr.onreadystatechange = () => {                                            
		if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
			resposta = (JSON.parse( xhr.response ))
			const author = resposta.result;
			document.getElementById("authorImg").value = author;		
			document.getElementById("authorImg").setAttribute("readonly", true);       
			}
		};

	
}