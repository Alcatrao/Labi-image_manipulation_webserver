function manipulateImage_gamma(file) {                       
    if(file != null) {
        sendFile_gamma(file);
    }
    else alert("Image missing!");
}

function sendFile_gamma(file) {
	
    var fator = document.getElementById("diff_gamma").valueAsNumber;


    if( fator == NaN || fator < 0 || fator > 255 || fator == "" || fator == undefined) {
        alert("Por favor insira um número válido (entre 0 e 60, decimal).");
    }
    else {

        var data = new FormData();
        data.append("file", file);
        data.append("f", fator);

                                
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/gamma");  


        xhr.onreadystatechange = () => {                                            //faz o .js esperar que o POST termine e o servidor envie uma resposta antes de continuar
            // Call a function when the state changes.
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                // Request finished. Do processing here.
                show_manipulated_image_gamma(JSON.parse( xhr.response ));       //o JSON.parse é essencial para usar a resposta como dicionário, como é pretendido
                }
            };

            xhr.send(data);

        }
}



function show_manipulated_image_gamma(response) {     //mostra a imagem  manipulada; resultado das 2 outros imagens

    
    document.getElementById("manipulated_image").innerHTML = "";            //limpar div para não ficar com várias imagens repetidas ao fazer múltiplos Manipulates na mesma página

    if (response["result"] != "gamma_falhou") {
        let image = document.createElement("img");
        image.src = "../"+response["result"];         //depois de muitas horas a falhar no carregamento da imagem para a página html, mesmo depois de trocar os caminhos de absolutos para relativos (e questionando-me se as imagens afinal estavam no cliente [as do updatePhoto e updatePhoto2 estão] ou no serviDor [como esta, e todas as que se possam buscar através do URL [endereço]]), apercebi-me que a pasta tmp não era dinâmica (essencial para usar os seus conteúdos para alterar cenas no serviDor
        image.width = "550";
        image.height = "450";
        document.getElementById("manipulated_image").appendChild(image);
    }
    else {
        alert("The chosen image could not have its gamma altered.");
    }
    

    
}


function im_inputs_gamma() {
    //criar input numérico (entre 0 e 255) para o parâmetro "diff"
    var divs = document.createElement("div");
    var textoDiff = document.createElement("input");
    textoDiff.type = "number";
    textoDiff.step = "0.1";
    textoDiff.min = "0";
    textoDiff.max = "60";
    textoDiff.id = "diff_gamma";
    textoDiff.style="color: blue";

    var labelFator = document.createElement("label");
    labelFator.innerHTML = "Please provide your desired gamma factor.";
    labelFator.setAttribute("for", textoDiff.id);


    divs.appendChild(labelFator);
    divs.appendChild(document.createElement("br"));
    divs.appendChild(textoDiff);



    //dar append deste div ao div escondido da página html
    document.getElementById("other_image").appendChild(divs);
    
}


export {manipulateImage_gamma, sendFile_gamma, show_manipulated_image_gamma, im_inputs_gamma};