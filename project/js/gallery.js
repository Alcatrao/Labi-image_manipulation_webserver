$(document).ready(
	function(){
		imageslist("all");
    });

function imageslist(id) {
	var author;
	if (id == "all") author = "all";
	else {
			author = $("#authorImg").val();		//o $ aqui serve como atalho para jQuery
			if (author == "") author = "all";
	}
	$.get("/list",
		{ id : author },
		function(response){
			showimages(response);
		});
}

function showimages(response) {
	// response.images is the list of dictionaries with the images information
	$("#showimages").html("");								//o código $() é funcionalmente semelhante ao document.getElementById() ??; é um atalho usado devido ao frequente uso do último, que é extenso de escrever. Mas também é usado para identificar variáveis (de modo a não serem confundidas com constantes, ou números), e nesse sentido, não tem significado para o interpretador; é como se fosse uma letra ou um underscore, e simplesmente serve para realçar ao leitor que existe uma variável onde está o símbolo. Além destes 2 casos, ainda pode ser usado como um placeholder, da mesma maneira que o {} é usado para formatar string em Python. Este símbolo também pode ser usado como atalho para a biblioteca jQuery
	for (let i = 0; i < response.images.length; i++) {
		// html code for print the image information
															//tive muitas dificuldades em fazer alguma coisa aparecer no div com id=showimages, mas quando finalmente apareceu algo, foi quando fiz o document.getElementById("showimages"), sem o #, em vez do ("#showimages"). Edit: só aparece algo se não houver erros no restante código; comentar a parte de mostrar a imagem é essencial se esta estiver mal
		
		const para = document.createElement("h3");
		const node = document.createTextNode("imagem "+response.images[i]["id"]+"; Nome: "+response.images[i]["name"]+"; Author: "+response.images[i]["author"]+"; "+response.images[i]["datetime"]);
		para.appendChild(node);

		const elexistente = document.getElementById("showimages");
		elexistente.appendChild(para);

		// html code for showing the image and allow to click on it and invoke function showimagecomments
		let img = document.createElement("img");				//esta linha cria uma imagem, que será apresentada como a imagem que tiver o caminho já abaixo especificador
		img.src = "../"+response.images[i]["path"];				//(Lembrança) caminho da imagem. Como o response.images é uma lista de dicionários, pode-se aceder a um elemento diretamente como se fosse um array ([i]) para obter um dicionário, e depois usar as chaves que todos os dicionários de imagens têm (id, author, name, path, datetime)
		img.onclick = function () {	showimagecomments(response.images[i]["id"]); }	//a propriedade .onclick recebe uma função, por isso cria-se uma função nova (sem nome; o javascript permite isso) que spawna a função showimagecomments, com argumento igual ao id da imagem na base de dados

		//img.height = 550;
		//img.width = 450;
		
		elexistente.appendChild(img);

		//o div na página gallery.html com id=showimages começa inicialmente vazio. Esta função cria novos elementos (parágrafos, headers, imagens) e dá append destes a esse div inicial. Estes novos elementos também podem levar append (isto pode ser feito de forma recursiva)
		

		
	}
}

function showimagecomments(id) {

	function get_page() {

		const queryString = window.location.search;
		const urlParams = new URLSearchParams(queryString);
		const userID = urlParams.get('userID')

		authenticate(userID)      
			
	}
	get_page()

	function authenticate(userID) {
		window.open('http://127.0.0.1:10013/page_image/?id=' + id+'&userID='+userID, '_blank');
	}
}
	
	

	//window.open("../html/image.html?id=" + id, '_blank');

