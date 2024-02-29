var file;       //serve para a função manipulateImage() poder saber se a var file está vazia ou não (não o consegue fazer se file não existir)
var file2;
//var contaDor = 0;   //visto que o .lastModified do objeto File não transfere para o ojecto Part em Python (que tem o .fileName e o .file), vou usar um contador para mudar os nomes das imagens que são criadas a partir das que são enviadas daqui do .js (cuja única variável que distingue os seus nomes, é o nome da 1ª imagem) juntamente com os seus dados, para resolver o problema de cashe da imagem manipulada, em que a aparece a imagem na cashe e não a que está na pasta tmp no servidor
                        //Edit: removi o contaDor e fiz com que (o nome d)a imagem manipulada fosse guardada com um timestamp desse momento, e que esse seu nome fosse devolvido no xhr.response; na resposta do servidor 
                        //Ao resolver o problema da cashe, as imagens manipuladas aparecem corretamente na página html, com o mesmo conteúdo que têm no servidor de onde são carregadas (e onde a cache intervém e guarda os seus caminhos para reutilização eficiente), mas assim ocupa-se mais memória
function updatePhoto(event) {                   //apresentar foto no lado esquerdo da página html quando ela for selecionada através do 'input type="file"'
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

	file = event.target.files[0];   //o event.target.files[0] representa o 1º (e neste caso, o único) ficheiro selecionado pelo utilizador no input que deu trigger a este evento. Está aqui a imagem selecionada pelo cliente em formato Blob (dados binários), que pode ser guardada e usada (e apresentada na página html, como é o caso) pelo servidor
	//Obtain the file               //a Blob, neste caso específico (em que é um File), contém as seguintes propriedades de relevo: o .file com os dados em si, o .name com o nome do ficheiro, e o .size (a Blob tem o .size, pelo que a File herda estes atributos) com o tamanho
	reader.readAsDataURL(file);
    return file;            //dados que devem chegar ao servidor
}



function manipulateImage_watermark() {                        //enviar foto ao servidor, que a deve ler, aplicar o método escolhido, e retornar a imagem manipulada (que será apresentada no lado direito da página html com o resultado do POST). Edit: não estava a funcionar porque tinha aqui 2 parâmetros de ficheiros criados em .js, que não existem na pagina html quando a função é chamada
    if(file != null && file2 != null) {
        sendFile_watermark(file, file2);
    }
    else alert("Image(s) missing!");
}

function sendFile_watermark(file, file2) {
	

	//obter falor de f e verificar se é válido
	var f = document.getElementById("watermark_texto").valueAsNumber;
    if( f == NaN || f < 0 || f > 1 || f == "" || f == undefined) {
        alert("Por favor insira um núemro válido.");
    }
    else {
									                            //o que é enviado é um ficheiro XML, com chaves e valores; as chaves devem ser iguais aos nomes dos parâmetros que a função do servidor aceita
                                                                //os valores são os dados que queremos enviar, e o nome da função do servidor é especificada no POST request abaixo
        
        var data = new FormData();
        data.append("file1", file);
        data.append("file2", file2);
        data.append("f", f);

								
		var xhr = new XMLHttpRequest();
		xhr.open("POST", "/watermark");  


        xhr.onreadystatechange = () => {                                            //faz o .js esperar que o POST termine e o servidor envie uma resposta antes de continuar
            // Call a function when the state changes.
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
              // Request finished. Do processing here.
              show_manipulated_image(JSON.parse( xhr.response ));       //o JSON.parse é essencial para usar a resposta como dicionário, como é pretendido
            }
          };

		xhr.upload.addEventListener("progress", updateProgress(window), false);       //enviar dados. Edit (possivelmente final): mudei o "this" que estava no updateProgress para "window", porque o "this" fica Undefined quando o scripting é modular (que passou a ser o caso desde que meti o handler a chamar as funções em vez deste script). Fiz um alert(this) com este script, e o valor era Window object (window)
        xhr.send(data);

            
	}
}

function updateProgress(evt){
	if(evt.loaded == evt.total) alert("Submitted successfully.");
}


function show_manipulated_image(response) {     //mostra a imagem  manipulada; resultado das 2 outros imagens

    
    document.getElementById("manipulated_image").innerHTML = "";            //limpar div para não ficar com várias imagens repetidas ao fazer múltiplos Manipulates na mesma página

    if (response["result"] != "watermark_falhou") {
        let water_image = document.createElement("img");
        water_image.src = "../"+response["result"];         //depois de muitas horas a falhar no carregamento da imagem para a página html, mesmo depois de trocar os caminhos de absolutos para relativos (e questionando-me se as imagens afinal estavam no cliente [as do updatePhoto e updatePhoto2 estão] ou no serviDor [como esta, e todas as que se possam buscar através do URL [endereço]]), apercebi-me que a pasta tmp não era dinâmica (essencial para usar os seus conteúdos para alterar cenas no serviDor
        water_image.width = "550";
        water_image.height = "450";
        document.getElementById("manipulated_image").appendChild(water_image);
    }
    else {
        alert("The 2 chosen images could not be manipulated into a watermarked image.");
    }
    

    
}















function updatePhoto2(event) {                    //apresentar foto que se pretenda inserir como watermark (quando selecionada esta opção) na foto original -- updatePhoto2
                                               
	/* imagem = new Image();
    imagem.src = event.target.result;
    contexto = document.getElementById("photo2").getContext("2d");
    imagem.onload = function () {contexto.drawImage(imagem, 0, 0, imagem.width, imagem.height, 0, 0, 550, 450);}; */

    //var file2;                              //a solução teve, como penúltimo passo antes de mostrar a imagem (antes de escrever o im_escolher.onchange=updatePhoto2), a escrita desta linha, a seguir à cópia da função uploadPhoto (e alterar o id de photo para photo2) para aqui. Edit: passei-a para cima, para possíveis checks por funções que não têm acesso ao local scope desta 
    var reader2 = new FileReader();
	reader2.onload = function(event) {
		//Create an imagem
		var img = new Image();
		img.onload = function() {
			//Put imagen on screen
			const canvas = $("#photo2")[0];
			const ctx = canvas.getContext("2d");
			ctx.drawImage(img,0,0,img.width,img.height,0,0,550, 450);
		}
		img.src = event.target.result;
	}

	file2 = event.target.files[0];
	//Obtain the file
	reader2.readAsDataURL(file2);
    
}


function im_watermark() {   //tinha um 'event' aqui dentro (depois da solução estar a funcionar, mas que nunca era usado)
   
    var divsFator = document.createElement("div");         //criar input para o utilizador meter um fator numérico de transparência da watermark
    var textoFator = document.createElement("input");
    textoFator.type = "number";
    textoFator.step = "0.1";
    textoFator.min = "0";
    textoFator.max = "1";
    textoFator.id = "watermark_texto";
    textoFator.style="color: blue";

    var labelFator = document.createElement("label");
    labelFator.innerHTML = "Fator de transparência (0 <= f <= 1)";
    labelFator.setAttribute("for", textoFator.id);


    divsFator.appendChild(textoFator);
    $("#other_image").append(labelFator);
    $("#other_image").append(divsFator);


    //a parte acima inclui os campos de texto que são precisos (além da imagem). Abaixo, cria-se o div com o input da 2ª imagem (watermark) e o respetivo canvas, que será atualizado com uma imagem quando esta for selecionada através da função iamginador


    var divs = document.createElement("div");        //tudo funciona, menos a imagem ser carregada para o canvas, pelo que nunca é mostrada na página html. Edit: ao final de umas 5 horas, consegui meter a imagem a aparecer. A solução era mudar a linha 'im_escolher.onchange = function () {updatePhoto2(event);};' (e 'im_escolher.onchange = "updatePhoto2(event)";') para 'im_escolher.onchange = updatePhoto2;'
    divs.setAttribute("class", "columnleft");

    var linebr = document.createElement("br");
    var header = document.createElement("h3");
    header.appendChild( document.createTextNode("Imagem a inserir na imagem principal"));

    var hr = document.createElement("hr");

    var im_escolher = document.createElement("input");
    im_escolher.type="file";
    im_escolher.accept="image/*";            //im_escolher.setAttribute("accept", "image/*");
    im_escolher.onchange = updatePhoto2;      //a solução para meter a imagem (2ª; a da watermark) na página html, ao final de tanto tempo, era simplesmente alterar esta linha para isto. Tirar as aspas, os parênteses (inputs), as functions, e meter apenas isto
                                            //a imagem que aparece para meter como watermark é alterada, bem como os dados da var file2 para corresponder aos dados da imagem aqui mostrada, pela função updatePhoto2. A imagem manipulada está a ser alterada em si (os seus dados são alterados), mas não está a levar update em novas Manipulates
    
    

        
    var im_canvas = document.createElement("canvas");   //cria o espaço onde vai ficar a 2ª imagem, mencionada acima 
    im_canvas.id = "photo2";
    im_canvas.width="550";
    im_canvas.height="450";

    divs.appendChild(linebr);
    divs.appendChild(header);
    divs.appendChild(hr);
    divs.appendChild(im_escolher);
    divs.appendChild(im_canvas);

    document.getElementById("other_image").appendChild(divs);
}



/* function im_modificador() {
    var modificador = document.getElementById("algo").value;
    $("#other_image").empty();        //também limpa as cenas da div da da 2ª imagem, para evitar acumulador
    $("#manipulated_image").empty();    //limpar o div onde fica a imagem manipulada
    if (modificador == "Watermark") {
        im_watermark();
     }
} */



function tmp_cleaner() {                    //alertar o servidor de que pode eliminar os conteúdos temp
    var xhr = new XMLHttpRequest();
	xhr.open("POST", "/tmp_cleaner");
    xhr.send();
    //esperar por resposta do servidor
     xhr.onreadystatechange = () => {                                            //faz o .js esperar que o POST termine e o servidor envie uma resposta antes de continuar
        // Call a function when the state changes.
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            window.close();
        }
    } 
    //var sair = confirm("Fechar página?");
    //if (sair == true)  window.close();
}




//Tudo o que está nesta linha e abaixo, foi adicionado para exportar o script para outro lado, para não ficar tudo cluttered
//este era o script .js invocado pela página .html com o mesmo nome, mas como se quer implementar outros métodos de manipulação de imagem além da watermark, para não preencher este script, importa-se este para um handler, juntamente com os scripts que se desenvolverem para outros métodos de processamento de imagem no servidor

//updatePhoto -> apresenta na página html a imagem selecionada pelo utilizador no "input" de imagem no "canvas" respetivo (o "input" e o "canvas" já estão presentes na página html, esta função preenche o "canvas" com os dados/imagem escolhido no "input")
//im_watermark -> cria um "div", "canvas", e um "input" de imagem e dá-lhes append num "div" debaixo do "div" (inicialmente vazio) com id="photo" (que já está presente), e "input" de texto para o fator de transparência (nenhum destes elementos está presenta na página html quando é carregada). Quando se escolhe uma imagem no "input" de imagem criado, chama-se a função "updatePhoto2"
//updatePhoto2 -> função semelhante a updatePhoto, mas que apresenta a imagem selecionada pelo utilizador no "input" de imagem criado pela função "im_watermark", no "canvas" criado pela mesma função, que está no "div" criado pela mesma função, que é appended no "div" inicialmente vazio da página html, abaixo do "div" da iamgem original
//sendFile_watermark -> envia um request /POST ao servidor, com os dados das 2 imagens escolhidas pelo utilizador, bem como o valor do fator de transparência escrito pelo utilizador no "input" de texto. Após o envio do /POST, é invocada a função "updateProgress" para sinalizar o envio total dos dados, e após tal, a função espera pela resposta do servidor, e caso esta indique sucesso por parte do servidor, invoca a "show_manipulated_image"
//show_manipulated_image -> lê a resposta do servidor (que é um parâmetro de entrada nesta função), e caso a resposta contenha o caminho relativo da imagem resultante da manipulação das 2 imagens previamente selecionadas e carregadas para variáveis com as funções "updatePhto" e "updatePhoto2", enviadas pelo "sendFile_watermark", cria e mostra essa imagem (que se encontra na pasta tmp/ do servidor, e as 2 imagens selecionadas pelo utilizador, estavam no computador do mesmo, mas após o envio do /POST, também são guardadas na tmp/ do servidor) num "div" já existente de início na página html (neste caso, não é criado um "canvas")

export {updatePhoto, im_watermark, updatePhoto2, manipulateImage_watermark, sendFile_watermark, updateProgress, show_manipulated_image, tmp_cleaner };