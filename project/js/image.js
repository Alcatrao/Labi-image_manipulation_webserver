var id;

$(document).ready(
    function(){
        const params = new URLSearchParams(window.location.search);
        id = params.get("id");

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
				const username = resposta.result;
				document.getElementById("user").value = username;		
				document.getElementById("user").setAttribute("readonly", true);
     
				}
		};


		

        imagecomments ();

    });      

function imagecomments() {
	$.get("/comments",
		{ idimg : id },
		function(response){
			showimageandinfo(response);
		});
}

function showimageandinfo(response) {
	// response.image is the image information
	document.getElementById("imageinfo").textContent='';			//limpar div, para atualizar com os novos valores (ao início não tem efeito, pois o div não tem elementos, mas quando se submete um novo comentário, isto impede que o conteúdo anterior seja repetido)

	let img = document.createElement("img");
	img.src = "../"+response.image["path"];
	img.height = 550;
	img.width = 900;

	let img_info = document.createElement("h2");
	let texto_node = document.createTextNode("imagem "+response.image["id"]+"; Nome: "+response.image["name"]+"; Author: "+response.image["author"]+"; "+response.image["datetime"]);

	document.getElementById("imageinfo").appendChild(img_info.appendChild(texto_node));
	document.getElementById("imageinfo").appendChild(img);


	// response.comments is the image list comments
	document.getElementById("comments").textContent='';			//limpar div, para atualizar com os novos valores (ao início não tem efeito, pois o div não tem elementos, mas quando se submete um novo comentário, isto impede que o conteúdo anterior seja repetido)

	for (let i=0; i<response.comments.length; i++) {
		let user_date = document.createElement("h3");
		let name_time = document.createTextNode(response.comments[i]["user"]+" at "+response.comments[i]["datetime"]);
		user_date.appendChild(name_time);

		let comment = document.createElement("h4");
		let texto = document.createTextNode(response.comments[i]["comment"]);
		comment.appendChild(texto);

		let section = document.createElement("div");
		document.getElementById("comments").appendChild(section.appendChild(user_date));
		document.getElementById("comments").appendChild(section.appendChild(comment));
	}

	// response.votes is the image votes
	document.getElementById("thumbs_up").textContent="";
	document.getElementById("thumbs_down").textContent='';

	let ups = document.createElement("p");
	let ups_number = document.createTextNode(response.votes["ups"]);

	let downs = document.createElement("p");
	let downs_number = document.createTextNode(response.votes["downs"]);

	document.getElementById("thumbs_up").appendChild(ups.appendChild(ups_number));
	document.getElementById("thumbs_down").appendChild(downs.appendChild(downs_number));

}

function newcomment() {
	// obtain the user and comment from image page

	var user = document.getElementById("user").value;				//escrever aqui o texto que tiver escrito no formulário quando o clique no botão que diz "Send Comment". Edit: depois do Login complexo, dar autofill a este campo
	var comment = document.getElementById("comment").value;
	
	if (user == "" || comment == "") alert("Missing comment and/or username!");
	else {
		$.post("/newcomment",
			{ idimg: id, username: user, newcomment: comment },		//antes estava aqui escrito, e nas funções upvote() e downvote() abaixo também, idimag em vez de idimg, o que me estava a causar confusão sobre o porquê de as coisas não funcionarem. Se o POST não for enviado com sucesso, os eventos associados também não ocorrem.
			function() { imagecomments(); });
	}
}

function upvote() {
	const queryString = window.location.search;
	const urlParams = new URLSearchParams(queryString);
	const userID = urlParams.get('userID');

	$.post("/upvote",
		{ idimg: id, userID: userID },
		function(response)
		{
			// update thumbs_up and thumbs_down
			document.getElementById("thumbs_up").textContent = parseInt(document.getElementById("thumbs_up").textContent)+JSON.parse(response).result;		//também fiquei aqui preso algum tempo até conseguir fazer o número incrementar onclick. Tudo o que foi preciso foi isto. Não sei explicar porque é que as outras soluções (como criar novo elemento com texto igual a response.votes["ups"] para dar append aqui, ou criar uma variável nova e fazer a soma com as devidas conversões) não funcionaram.
		});
}

function downvote() {
	const queryString = window.location.search;
	const urlParams = new URLSearchParams(queryString);
	const userID = urlParams.get('userID');

	$.post("/downvote",
		{ idimg: id, userID: userID },
		function(response)
		{
			// update thumbs_up and thumbs_down	
			document.getElementById("thumbs_down").textContent = parseInt(document.getElementById("thumbs_down").textContent)+JSON.parse(response).result;
		});
}
