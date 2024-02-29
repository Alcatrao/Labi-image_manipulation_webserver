function manipulateImage_vignette(file) {                        //enviar foto ao servidor, que a deve ler, aplicar o método escolhido, e retornar a imagem manipulada (que será apresentada no lado direito da página html com o resultado do POST). Edit: não estava a funcionar porque tinha aqui 2 parâmetros de ficheiros criados em .js, que não existem na pagina html quando a função é chamada
    if(file != null) {
        sendFile_vignette(file);
    }
    else alert("Image missing!");
}

function sendFile_vignette(file) {
	
    var data = new FormData();
    data.append("file", file)
    
							
	var xhr = new XMLHttpRequest();
	xhr.open("POST", "/vignette");  


    xhr.onreadystatechange = () => {                                            //faz o .js esperar que o POST termine e o servidor envie uma resposta antes de continuar
        // Call a function when the state changes.
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            // Request finished. Do processing here.
            show_manipulated_image_vignette(JSON.parse( xhr.response ));       //o JSON.parse é essencial para usar a resposta como dicionário, como é pretendido
            }
        };

        xhr.send(data);

            
}



function show_manipulated_image_vignette(response) {     //mostra a imagem  manipulada; resultado das 2 outros imagens

    
    document.getElementById("manipulated_image").innerHTML = "";            //limpar div para não ficar com várias imagens repetidas ao fazer múltiplos Manipulates na mesma página

    if (response["result"] != "vignette_falhou") {
        let image = document.createElement("img");
        image.src = "../"+response["result"];         //depois de muitas horas a falhar no carregamento da imagem para a página html, mesmo depois de trocar os caminhos de absolutos para relativos (e questionando-me se as imagens afinal estavam no cliente [as do updatePhoto e updatePhoto2 estão] ou no serviDor [como esta, e todas as que se possam buscar através do URL [endereço]]), apercebi-me que a pasta tmp não era dinâmica (essencial para usar os seus conteúdos para alterar cenas no serviDor
        image.width = "550";
        image.height = "450";
        document.getElementById("manipulated_image").appendChild(image);
    }
    else {
        alert("The chosen image could not be vignetted.");
    }
    

    
}


export {manipulateImage_vignette, sendFile_vignette, show_manipulated_image_vignette};